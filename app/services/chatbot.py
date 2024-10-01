import re
import logging
from typing import Optional, Tuple
from flask import Blueprint, request, jsonify
from config import DB_CONFIG
from app.models.financial_data import FinancialDataAccess
from datetime import datetime

# Define the chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__)

class ChatbotError(Exception):
    """Custom exception for Chatbot-related errors."""
    pass

# Initialize FinancialDataAccess
financial_data_access = FinancialDataAccess(DB_CONFIG)

def fetch_financial_data(company_name: str, year: Optional[int] = None) -> Optional[dict]:
    """Fetch financial data for a given company and year from the database."""
    try:
        data = financial_data_access.get_financial_data(company_name, year)
        return data
    except Exception as e:
        logging.error(f"An error occurred while fetching financial data: {e}")
        return None

def calculate_percentage_change(company: str, metric: str, start_year: int, end_year: int) -> Optional[float]:
    """Calculate the percentage change in a financial metric between two years."""
    try:
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
                    logging.warning(f"ZeroDivisionError for {metric} of {company} from {start_year} to {end_year}")
                    return None
    except Exception as e:
        logging.error(f"An error occurred while calculating percentage change: {e}")
    return None

def extract_year_from_question(question: str) -> Optional[int]:
    """Extract the year from the question if mentioned, or default to current year."""
    match = re.search(r'(\d{4})', question)
    if match:
        return int(match.group(1))
    return None

def extract_company_and_metric(question: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract the company and metric from the question."""
    companies = ['Apple', 'Microsoft', 'Tesla']
    metrics = {
        'revenue': 'total_revenue',
        'net income': 'net_income',
        'assets': 'total_assets',
        'liabilities': 'total_liabilities',
        'cash flow from operating activities': 'cash_flow_from_operating_activities'
    }

    company = None
    metric = None

    for comp in companies:
        if comp.lower() in question.lower():
            company = comp
            break

    for key, value in metrics.items():
        if key in question.lower():
            metric = value
            break

    return company, metric

def process_question(question: str) -> Optional[str]:
    """Process the user's question and generate a response based on financial data."""
    try:
        # Extract company, metric, and year from the question
        company, metric = extract_company_and_metric(question)
        year = extract_year_from_question(question) or datetime.now().year

        if not company or not metric:
            raise ChatbotError("Could not understand the company or financial metric from the question.")

        # Handle percentage change requests
        match = re.search(r'percentage change in (\w+) for (\w+) from (\d{4}) to (\d{4})', question, re.IGNORECASE)
        if match:
            metric_name, company, start_year, end_year = match.groups()
            change = calculate_percentage_change(company, metric_name, int(start_year), int(end_year))
            if change is not None:
                return f"The percentage change in {metric_name} for {company} from {start_year} to {end_year} is {change:.1f}%."
            else:
                raise ChatbotError("Data for the specified metric or years is not available.")

        # Fetch the financial data for the company and year
        data = fetch_financial_data(company, year)
        if data and metric in data:
            return f"{company}'s {metric.replace('_', ' ')} for {year} was ${data.get(metric, 'N/A'):,} million."

        raise ChatbotError("Data for the specified company, metric, or year is not available.")
    
    except ChatbotError as e:
        logging.error(f"An error occurred while processing the question: {e}")
        return str(e)
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing the question: {e}")
        return "An error occurred while processing your request."

@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    """Endpoint for asking questions to the chatbot."""
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is required'}), 400

    question = data['question']
    try:
        answer = process_question(question)
        return jsonify({'answer': answer}), 200
    except ChatbotError as e:
        return jsonify({'error': str(e)}), 500
