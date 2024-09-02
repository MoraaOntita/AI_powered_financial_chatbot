from data_access.financial_data import financial_data_access
from data_access.qa_pairs import qa_data_access

def get_answer(question):
    # Check if the question matches a known QA pair
    answer = qa_data_access.get_qa_pair(question)
    if answer:
        return answer

    # Example rule-based logic if QA pair does not exist
    if 'total revenue' in question and 'Microsoft' in question and '2023' in question:
        data = financial_data_access.get_financial_data('Microsoft', 2023)
        if data:
            return f"The total revenue for Microsoft in 2023 is {data[0]} million."
        else:
            return "No financial data available for Microsoft in 2023."
    
    return "Sorry, I couldn't find an answer to your question."

if __name__ == "__main__":
    while True:
        question = input("Ask a financial question: ")
        answer = get_answer(question)
        print(answer)
