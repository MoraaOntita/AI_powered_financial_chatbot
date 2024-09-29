from src.data_access.qa_pairs import QADataAccess
from config import DB_CONFIG

class QARules:
    def __init__(self):
        self.qa_data_access = QADataAccess(DB_CONFIG)  # Create an instance of QADataAccess

    def get_qa_answer(self, question: str) -> str:
        answer = self.qa_data_access.get_qa_pair(question)  # Call the method on the instance
        return answer or "Sorry, I couldn't find an answer to your question."

# Instantiate with dependency injection if needed
qa_rules = QARules()
