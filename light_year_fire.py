from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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

@app.post("/calculate")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
