import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm

# Configure page settings
st.set_page_config(
    page_title="Black-Scholes Option Pricer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main application header
st.title("Black-Scholes Option Pricer")

# Application overview in the main page
st.header("Black-Scholes Model Inputs")

col1, col2, col3 = st.columns([1,1,1], gap="small")

with col1:
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

class BlackScholes:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(self):
        d1 = (np.log(self.current_price / self.strike) + (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        call_price = self.current_price * norm.cdf(d1) - self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)
        put_price = self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - self.current_price * norm.cdf(-d1)
        return call_price, put_price


bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()