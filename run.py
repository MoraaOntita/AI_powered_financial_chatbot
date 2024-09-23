from app import create_app
import logging

# Initialize the app using the factory method
app = create_app()

if __name__ == "__main__":
    # Set logging level for the app
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Log the start of the app
    app.logger.info("Starting the BCG Chatbot application...")

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
