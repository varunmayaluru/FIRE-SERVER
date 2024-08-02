from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class RetirementDetails(BaseModel):
    current_monthly_expenses: float
    current_age: int
    retirement_age: int
    expected_life_span: int
    current_investments: float
    expected_inflation: float
    post_retirement_return: float
    pre_retirement_return: float


class FinancialInfo(BaseModel):
    age: int
    current_savings: float
    saving_monthly: float
    stock_allocation: float
    stock_growth: float
    bond_allocation: float
    bond_growth: float
    cash_allocation: float
    annual_spending: float
    withdrawal_rate: float

@app.post("/fire_calculator_financials")
def calculate_financials(info: FinancialInfo):
    # Calculate annual savings
    annual_savings = info.saving_monthly * 12

    # Calculate FIRE target
    fire_target = info.annual_spending / (info.withdrawal_rate / 100)

    # Effective overall rate of return
    effective_rate_of_return = (
        (info.stock_allocation * info.stock_growth) +
        (info.bond_allocation * info.bond_growth) +
        (info.cash_allocation * 0)
    ) / 100

    # Calculate the number of years to reach FIRE target
    current_savings = info.current_savings
    years = 0
    while current_savings < fire_target:
        current_savings += annual_savings
        current_savings *= (1 + effective_rate_of_return)
        years += 1
        if years > 100:  # Prevent infinite loop
            raise HTTPException(status_code=400, detail="Calculation took too long. Check your input values.")

    retirement_age = info.age + years

    return {
        "fire_target": fire_target,
        "retirement_age": retirement_age,
        "annual_savings": annual_savings
    }


@app.post("/fire_calculator_retirement")
def calculate_retirement(details: RetirementDetails):
    # Step 1: Calculate Monthly Expense at Retirement
    future_expense = details.current_monthly_expenses * (1 + details.expected_inflation / 100) ** (details.retirement_age - details.current_age)

    # Step 2: Calculate Corpus Required for Post-Retirement Period
    post_retirement_period = details.expected_life_span - details.retirement_age
    monthly_return_rate_post = details.post_retirement_return / 100 / 12
    corpus_required = future_expense * ((1 - (1 + monthly_return_rate_post) ** (-post_retirement_period * 12)) / monthly_return_rate_post)

    # Step 3: Calculate Future Value of Current Investments
    future_value_of_current_investments = details.current_investments * (1 + details.pre_retirement_return / 100) ** (details.retirement_age - details.current_age)

    # Step 4: Calculate Corpus to be Built
    corpus_to_be_built = corpus_required - future_value_of_current_investments

    # Step 5: Calculate Monthly Investment Needed
    monthly_return_rate_pre = details.pre_retirement_return / 100 / 12
    number_of_months = (details.retirement_age - details.current_age) * 12
    monthly_investment_needed = corpus_to_be_built * monthly_return_rate_pre / ((1 + monthly_return_rate_pre) ** number_of_months - 1)

    return {
        "monthly_expense_at_retirement": round(future_expense, 2),
        "future_value_of_current_investments": round(future_value_of_current_investments, 2),
        "corpus_required_for_post_retirement": round(corpus_required, 2),
        "corpus_to_be_built": round(corpus_to_be_built, 2),
        "monthly_investment_needed": round(monthly_investment_needed, 2)
    }

# To run the application, use: uvicorn retirement_calculator:app --reload
## INPUT JSON 
"""
{
  "current_monthly_expenses": 50000,
  "current_age": 25,
  "retirement_age": 60,
  "expected_life_span": 75,
  "current_investments": 200000,
  "expected_inflation": 4.5,
  "post_retirement_return": 4.5,
  "pre_retirement_return": 7.5
}

{
  "age": 30,
  "current_savings": 20000,
  "saving_monthly": 1000,
  "stock_allocation": 0.7,
  "stock_growth": 6,
  "bond_allocation": 0.2,
  "bond_growth": 4,
  "cash_allocation": 0.1,
  "annual_spending": 40000,
  "withdrawal_rate": 4
}

"""