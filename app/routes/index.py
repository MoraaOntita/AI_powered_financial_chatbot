from flask import Blueprint, render_template, jsonify, request, current_app
from typing import Any, Dict
import logging

# Define the Blueprint for the main routes
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
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

@index_bp.route('/ask', methods=['POST'])
def ask_question() -> Any:
    """
    Route to handle questions sent to the chatbot.

    This route expects a JSON payload with a 'question' field. It will pass the question
    to the chatbot service and return the response.

    Returns:
        Any: JSON response containing the chatbot's answer or an error message.
    """
    try:
        # Ensure the request content is in JSON format
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        # Get the incoming JSON data
        data = request.get_json()

        # Log the received data to help with debugging
        current_app.logger.info(f"Received data: {data}")

        # Check if data is a dictionary, otherwise raise an error
        if not isinstance(data, dict):
            raise ValueError(f"Expected data to be a dictionary, but got {type(data)} instead.")

        # Get the 'question' key from the data
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        # Call the chatbot service to get an answer
        from app.services.chatbot import process_question
        answer = process_question(question)

        # Log the answer to help with debugging
        current_app.logger.info(f"Processed answer: {answer}")

        return jsonify({'question': question, 'answer': answer})

    except ValueError as e:
        # Handle cases where data isn't the expected type
        current_app.logger.error(f"ValueError: {e}")
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        # Log any other exceptions and return a 500 error
        current_app.logger.error(f"An error occurred while processing the question: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
