from flask import Blueprint, render_template, jsonify, request, current_app
from typing import Any, Dict
import logging

# Define the Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index() -> str:
    """
    The main route that serves the homepage.

    Returns:
        str: Rendered HTML content for the homepage.
    """
    try:
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error(f"Error rendering index.html: {e}")
        return "An error occurred while loading the page.", 500

@main.route('/api/ask', methods=['POST'])
def ask_question() -> Any:
    """
    Route to handle questions sent to the chatbot.

    This route expects a JSON payload with a 'question' field. It will pass the question
    to the chatbot service and return the response.

    Returns:
        Any: JSON response containing the chatbot's answer or an error message.
    """
    try:
        data: Dict[str, Any] = request.get_json()
        question: str = data.get('question', '')

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        # Here you would typically call a service to handle the question and get an answer.
        # For example:
        from app.services.chatbot import process_question
        answer = process_question(question)

        return jsonify({'question': question, 'answer': answer})
    except KeyError as e:
        current_app.logger.error(f"Missing key in request data: {e}")
        return jsonify({'error': f"Missing key: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.error(f"An error occurred while processing the question: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
