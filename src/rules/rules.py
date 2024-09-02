from rules.financial_rules import FinancialRules
from rules.qa_rules import QARules

class RulesEngine:
    def __init__(self):
        self.financial_rules = FinancialRules()
        self.qa_rules = QARules()

    def apply_rules(self, question: str) -> str:
        # Check QA pairs first
        answer = self.qa_rules.get_qa_answer(question)
        if answer and "Sorry, I couldn't find an answer to your question." not in answer:
            return answer

        # Apply financial rules
        if 'total revenue' in question:
            if 'Microsoft' in question and '2023' in question:
                return self.financial_rules.get_revenue('Microsoft', 2023)
            elif 'Tesla' in question and '2023' in question:
                return self.financial_rules.get_revenue('Tesla', 2023)
            elif 'Apple' in question and '2023' in question:
                return self.financial_rules.get_revenue('Apple', 2023)

        if 'net income' in question:
            if 'Tesla' in question and '2022' in question:
                return self.financial_rules.get_net_income('Tesla', 2022)
            elif 'Microsoft' in question and '2021' in question:
                return self.financial_rules.get_net_income('Microsoft', 2021)
            elif 'Apple' in question and '2021' in question:
                return self.financial_rules.get_net_income('Apple', 2021)

        if 'total assets' in question:
            if 'Microsoft' in question and '2023' in question:
                return self.financial_rules.get_total_assets('Microsoft', 2023)
            elif 'Apple' in question and '2021' in question:
                return self.financial_rules.get_total_assets('Apple', 2021)

        if 'total liabilities' in question:
            if 'Tesla' in question and '2023' in question:
                return self.financial_rules.get_total_liabilities('Tesla', 2023)
            elif 'Microsoft' in question and '2022' in question:
                return self.financial_rules.get_total_liabilities('Microsoft', 2022)

        if 'cash flow' in question:
            if 'Apple' in question and '2022' in question:
                return self.financial_rules.get_cash_flow('Apple', 2022)

        if 'percentage change' in question:
            if 'Microsoft' in question and '2021' in question and '2022' in question:
                return self.financial_rules.get_percentage_change_in_net_income('Microsoft', 2021, 2022)

        return "Sorry, I couldn't find an answer to your question."

# Instantiate with dependency injection if needed
rules_engine = RulesEngine()