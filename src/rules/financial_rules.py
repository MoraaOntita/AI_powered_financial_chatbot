from data_access.financial_data import get_financial_data
from typing import Optional

class FinancialRules:
    def __init__(self):
        pass

    def get_revenue(self, company_name: str, year: int) -> str:
        data = get_financial_data(company_name, year)
        if data:
            return f"The total revenue for {company_name} in {year} is {data[0]} million."
        return "Data not available."

    def get_net_income(self, company_name: str, year: int) -> str:
        data = get_financial_data(company_name, year)
        if data:
            return f"The net income for {company_name} in {year} is {data[1]} million."
        return "Data not available."

    def get_total_assets(self, company_name: str, year: int) -> str:
        data = get_financial_data(company_name, year)
        if data:
            return f"The total assets for {company_name} in {year} are {data[2]} million."
        return "Data not available."

    def get_total_liabilities(self, company_name: str, year: int) -> str:
        data = get_financial_data(company_name, year)
        if data:
            return f"The total liabilities for {company_name} in {year} are {data[3]} million."
        return "Data not available."

    def get_cash_flow(self, company_name: str, year: int) -> str:
        data = get_financial_data(company_name, year)
        if data:
            return f"The cash flow from operating activities for {company_name} in {year} is {data[4]} million."
        return "Data not available."

    def get_percentage_change_in_net_income(self, company_name: str, start_year: int, end_year: int) -> str:
        start_data = get_financial_data(company_name, start_year)
        end_data = get_financial_data(company_name, end_year)
        if start_data and end_data:
            start_income = start_data[1]
            end_income = end_data[1]
            if start_income == 0:
                return "No data available for percentage change calculation."
            percentage_change = ((end_income - start_income) / start_income) * 100
            return f"The percentage change in net income for {company_name} from {start_year} to {end_year} is {percentage_change:.1f}%."
        return "Data not available."

# Instantiate with dependency injection if needed
financial_rules = FinancialRules()