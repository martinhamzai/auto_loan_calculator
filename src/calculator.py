import pandas as pd
import streamlit as st

def calculate(auto_value: int, deposit: int, rate: float, n: int) -> tuple[float, float, float]:
    """
    Calculates the payments in an auto loan.

    Parameters:
        auto_value (int): Total value of the auto.
        deposit (int): Down payment.
        rate (float): Annual interest rate (in percentage points).
        n (int): Loan term in months.

    Returns:
        tuple[float, float, float]: Montly payment, total payment, and total interest.
    """
    p = auto_value - deposit
    r = rate / 100 / 12
    
    if r == 0: 
        m = p / n
    else:
        m = p * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    
    total_payment = m * n
    total_interest = total_payment - p

    return m, total_payment, total_interest

def create_df(auto_value: int, deposit: int, rate:float, n: int, m: float) -> pd.DataFrame:
    """
    Create a DataFrame with the repayment schedule.

    Parameters:
        auto_value (int): Total value of the auto.
        deposit (int): Down payment.
        rate (float): Annual interest rate (in percentage points).
        n (int): Loan term in months.
        m (float): Monthly payment.

    Returns:
        pd.DataFrame: A DataFrame containing the repayment schedule with remaining balances.
    """
    
    p = auto_value - deposit
    r = rate / 100 / 12
    schedule = []
    for i in range(1, n+1):
        p -= m - p * r
        schedule.append([i, round(p, 2)])
    return pd.DataFrame(schedule, columns=["Month","Remaining Balance"])

if __name__ == "__main__":
    st.set_page_config("Auto Loan Calculator",
                       page_icon="🚗")
    st.title("Auto Loan Calculator🚗")

    st.write("### Values")
    col1, col2 = st.columns(2)
    auto_value = col1.number_input("💲 Auto Value", 
                                  min_value=0, 
                                  max_value=int(10e6),
                                  step=1000)
    deposit = col1.number_input("💲 Down Payment",
                                min_value=0,
                                max_value=auto_value,
                                step=1000)
    rate = col2.number_input("Interest Rate",
                             min_value=0.0,
                             max_value=100.0,
                             step=0.1)
    term = col2.number_input("Loan Term (Months)",
                             min_value=1,
                             max_value=120)
    
    m, total_payment, total_interest = calculate(auto_value, deposit, rate, term)

    st.write("### Payments")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Monthly Payments", value=f"${m:,.2f}")
    col2.metric(label="Total Payment", value=f"${total_payment:,.2f}")
    col3.metric(label="Total Interest", value=f"${total_interest:,.2f}")

    st.write("### Payment Schedule")
    df = create_df(auto_value, deposit, rate, term, m)
    df = df.groupby("Month").min()
    st.line_chart(df)