from typing import Optional
import logging
from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import DictCursor
from config import DB_CONFIG

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
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                query = """
                SELECT company_name, year, total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
                FROM financial_data
                WHERE company_name = %s
                """
                params = [company_name]
                if year:
                    query += " AND year = %s"
                    params.append(year)
                cur.execute(query, tuple(params))
                result = cur.fetchone()
                return dict(result) if result else None
    except Exception as e:
        logging.error(f"An error occurred while fetching financial data: {e}")
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
        # Placeholder for parsing logic; this would typically involve NLP or keyword matching
        if "Microsoft" in question and "revenue" in question:
            data = fetch_financial_data("Microsoft", 2023)
            if data:
                return f"Microsoft's revenue for 2023 was ${data['total_revenue']:,} million."
        
        # Example for other queries
        if "Tesla" in question and "net income" in question:
            data = fetch_financial_data("Tesla", 2023)
            if data:
                return f"Tesla's net income for 2023 was ${data['net_income']:,} million."

        return "I'm not sure about that. Could you please ask something else?"
    except Exception as e:
        logging.error(f"An error occurred while processing the question: {e}")
        return None

# Define a route for asking questions
@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    answer = process_question(question)
    return jsonify({'answer': answer})
