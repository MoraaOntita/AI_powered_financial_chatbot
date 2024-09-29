from src.data_access.financial_data import financial_data_access
from typing import Optional

class FinancialRules:
    def __init__(self):
        pass

    def get_revenue(self, company_name: str, year: int) -> str:
        data = financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The total revenue for {company_name} in {year} is {data['total_revenue']} million."
        return "Data not available."

    def get_net_income(self, company_name: str, year: int) -> str:
        data = financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The net income for {company_name} in {year} is {data['net_income']} million."
        return "Data not available."

    def get_total_assets(self, company_name: str, year: int) -> str:
        data = financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The total assets for {company_name} in {year} are {data['total_assets']} million."
        return "Data not available."

    def get_total_liabilities(self, company_name: str, year: int) -> str:
        data = financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The total liabilities for {company_name} in {year} are {data['total_liabilities']} million."
        return "Data not available."

    def get_cash_flow(self, company_name: str, year: int) -> str:
        data = financial_data_access.get_financial_data(company_name, year)
        if data:
            return f"The cash flow from operating activities for {company_name} in {year} is {data['cash_flow_from_operating_activities']} million."
        return "Data not available."

    def get_percentage_change_in_net_income(self, company_name: str, start_year: int, end_year: int) -> str:
        start_data = financial_data_access.get_financial_data(company_name, start_year)
        end_data = financial_data_access.get_financial_data(company_name, end_year)
        if start_data and end_data:
            start_income = start_data['net_income']
            end_income = end_data['net_income']
            if start_income == 0:
                return "No data available for percentage change calculation."
            percentage_change = ((end_income - start_income) / start_income) * 100
            return f"The percentage change in net income for {company_name} from {start_year} to {end_year} is {percentage_change:.1f}%."
        return "Data not available."

# Instantiate with dependency injection if needed
financial_rules = FinancialRules()
