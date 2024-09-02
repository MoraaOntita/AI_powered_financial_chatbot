from data_access.qa_pairs import get_qa_pair

class QARules:
    def __init__(self):
        pass

    def get_qa_answer(self, question: str) -> str:
        answer = get_qa_pair(question)
        return answer or "Sorry, I couldn't find an answer to your question."

# Instantiate with dependency injection if needed
qa_rules = QARules()