from typing import Protocol, Optional
from app.models.financial_data import FinancialDataAccess
from app.models.qa_pairs import QADataAccess
from config import DB_CONFIG

class DataAccessProtocol(Protocol):
    def get_financial_data(self, company_name: str, year: int) -> Optional[tuple]:
        ...

    def get_qa_pair(self, question: str) -> str:
        ...

class ChatBotService:
    def __init__(self, financial_data_access: DataAccessProtocol, qa_data_access: DataAccessProtocol):
        self.financial_data_access = financial_data_access
        self.qa_data_access = qa_data_access

    def _get_financial_answer(self, company_name: str, year: int) -> str:
        """Helper method to fetch financial data and format it."""
        data = self.financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The total revenue for {company_name} in {year} is {data[0]} million."
        else:
            return f"No financial data available for {company_name} in {year}."

    def get_answer(self, question: str) -> str:
        """Main method to get an answer to the given question."""
        # Check if the question matches a known QA pair
        answer = self.qa_data_access.get_qa_pair(question)
        if answer:
            return answer

        # Example rule-based logic if QA pair does not exist
        if 'total revenue' in question:
            company_name = 'Microsoft'  # Hardcoded for demonstration; would be extracted from question in a real case
            year = 2023  # Hardcoded for demonstration; would be extracted from question in a real case
            return self._get_financial_answer(company_name, year)
        
        return "Sorry, I couldn't find an answer to your question."

# Dependency Injection
financial_data_access = FinancialDataAccess(DB_CONFIG)
qa_data_access = QADataAccess(DB_CONFIG)
chatbot_service = ChatBotService(financial_data_access, qa_data_access)

def get_answer(question: str) -> str:
    """Function to be used by the Flask route."""
    return chatbot_service.get_answer(question)
