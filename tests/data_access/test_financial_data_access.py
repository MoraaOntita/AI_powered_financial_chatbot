from src.data_access.financial_data import financial_data_access

def test_get_financial_data():
    company_name = 'Microsoft'
    year = 2023
    data = financial_data_access.get_financial_data(company_name, year)
    print(data)

def test_get_qa_pairs():
    company_name = 'Microsoft'
    year = 2023
    qa_pairs = financial_data_access.get_qa_pairs(company_name, year)
    print(qa_pairs)

if __name__ == "__main__":
    test_get_financial_data()
    test_get_qa_pairs()
