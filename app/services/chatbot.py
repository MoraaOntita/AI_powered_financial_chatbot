import re
import logging
from typing import Optional
from flask import Blueprint, request, jsonify
from config import DB_CONFIG
from src.data_access.financial_data import financial_data_access

# Define the chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__)

class ChatbotError(Exception):
    """Custom exception for Chatbot-related errors."""
    pass

def fetch_financial_data(company_name: str, year: Optional[int] = None) -> Optional[dict]:
    """
    Fetch financial data for a given company and year from the database.

    Args:
        company_name (str): The name of the company.
        year (Optional[int]): The year for which the financial data is required. Defaults to None.

    Returns:
        Optional[dict]: A dictionary containing the financial data if found, None otherwise.
    """
    try:
        data = financial_data_access.get_financial_data(company_name, year)
        return data
    except Exception as e:
        logging.error(f"An error occurred while fetching financial data: {e}")
        return None

def calculate_percentage_change(company: str, metric: str, start_year: int, end_year: int) -> Optional[float]:
    """
    Calculate the percentage change in a financial metric between two years.

    Args:
        company (str): The name of the company.
        metric (str): The financial metric to calculate the change for.
        start_year (int): The starting year.
        end_year (int): The ending year.

    Returns:
        Optional[float]: The percentage change in the financial metric, or None if data is not available.
    """
    data_start = fetch_financial_data(company, start_year)
    data_end = fetch_financial_data(company, end_year)
    
    if data_start and data_end:
        start_value = data_start.get(metric)
        end_value = data_end.get(metric)
        if start_value is not None and end_value is not None:
            try:
                change = ((end_value - start_value) / start_value) * 100
                return change
            except ZeroDivisionError:
                return None
    return None

def extract_year_from_question(question: str) -> Optional[int]:
    """
    Extract the year from the question if it asks for the last year available.

    Args:
        question (str): The question input by the user.

    Returns:
        Optional[int]: The last year available or None if not specified.
    """
    match = re.search(r'last year available', question, re.IGNORECASE)
    if match:
        # Assume the latest year available in your data; replace with dynamic fetching if possible
        return 2023  # Change this as needed based on your data
    return None

def process_question(question: str) -> Optional[str]:
    """
    Process the user's question and generate a response based on financial data.

    Args:
        question (str): The question input by the user.

    Returns:
        Optional[str]: The chatbot's response to the question. Returns None if an error occurs.
    """
    try:
        # Check for percentage change requests
        match = re.search(r'percentage change in (\w+) for (\w+) from (\d{4}) to (\d{4})', question, re.IGNORECASE)
        if match:
            metric, company, start_year, end_year = match.groups()
            change = calculate_percentage_change(company, metric, int(start_year), int(end_year))
            if change is not None:
                return f"The percentage change in {metric} for {company} from {start_year} to {end_year} is {change:.1f}%."
            else:
                return "Data for the specified metric or years is not available."

        # Handle questions asking for specific financial metrics with dynamic year
        year = extract_year_from_question(question)
        if not year:
            year = 2023  # Default year if no dynamic year found

        if "revenue" in question:
            if "Apple" in question:
                data = fetch_financial_data("Apple", year)
                if data:
                    return f"Apple's total revenue for {year} was ${data.get('total_revenue', 'N/A'):,} million."
            elif "Microsoft" in question:
                data = fetch_financial_data("Microsoft", year)
                if data:
                    return f"Microsoft's total revenue for {year} was ${data.get('total_revenue', 'N/A'):,} million."
        
        elif "net income" in question:
            if "Tesla" in question:
                data = fetch_financial_data("Tesla", year)
                if data:
                    return f"Tesla's net income for {year} was ${data.get('net_income', 'N/A'):,} million."
        
        elif "total assets" in question:
            if "Apple" in question:
                data = fetch_financial_data("Apple", year)
                if data:
                    return f"Apple's total assets for {year} were ${data.get('total_assets', 'N/A'):,} million."
        
        # Default response for unsupported queries
        return ("I'm only able to answer questions about Microsoft, Tesla, and Apple "
                "for the year 2023. Please ask about their revenue, net income, or other "
                "financial metrics.")
    except Exception as e:
        logging.error(f"An error occurred while processing the question: {e}")
        return "An error occurred while processing your request."

# Define a route for asking questions
@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    answer = process_question(question)
    return jsonify({'answer': answer})
