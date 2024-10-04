# AI_powered_financial_chatbot

## Overview

Welcome to the **BCG Chatbot**! This application is designed to assist users with financial queries related to **Microsoft**, **Tesla**, and **Apple** for the year **2023**. Whether you're looking for information about revenue, net income, total assets, or other financial metrics, the BCG Chatbot is here to help!

## Features

- **Interactive Chat Interface**: Users can ask questions in a user-friendly chatbox and receive informative answers.
- **Database Integration**: Utilizes PostgreSQL to store and retrieve financial data dynamically.
- **Data Insertion**: Automated scripts to insert financial data and question-answer pairs for improved responses.
- **Environment Configuration**: Uses a `.env` file to manage environment variables securely.


## Requirements

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose
- Python 3.11+
- PostgreSQL (if not using Docker)

## Getting Started

### 1. Clone the Repository

    ```bash
    git clone https://github.com/MoraaOntita/AI_powered_financial_chatbot
    cd BCG-Chatbot
    ```


### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

- POSTGRES_DB=<your_database_name>
- POSTGRES_USER=<your_username>
- POSTGRES_PASSWORD=<your_password>
- FLASK_APP=run.py
- FLASK_ENV=development
- SECRET_KEY=<your_secret_key>


### 3. Build and Run the Application

Using Docker Compose, you can build and run the application with the following command:

```bash
docker-compose up --build
```

### 4. Access the Chatbot

Open your web browser and navigate to http://localhost:5001 to start interacting with the BCG Chatbot.

## Scripts
### Data Insertion Scripts
- `insert_financial_data.py`: This script inserts financial data from a CSV file into the PostgreSQL database.
- `insert_qa_pairs.py`: This script inserts predefined question-answer pairs into the database to enhance the chatbot's responses.

### Wait for PostgreSQL Script
- `wait-for-postgres.sh`: A utility script that checks if the PostgreSQL database is ready before executing any commands.

## Contributing
Contributions are welcome! If you would like to contribute to the BCG Chatbot, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or inquiries, feel free to reach out:

Email: nyamusiontita@gmail.command

#### Happy Coding!
