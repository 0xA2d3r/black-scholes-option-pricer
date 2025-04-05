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

st.title("Black-Scholes Option Pricer")

class BlackScholes:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_d1_d2(self):
        d1 = (
            np.log(self.current_price / self.strike) + 
            (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity
        ) / (self.volatility * np.sqrt(self.time_to_maturity))

        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)

        return d1, d2

    def calculate_prices(self):
        d1, d2 = self.calculate_d1_d2()
        
        call_price = self.current_price * norm.cdf(d1) - self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)

        put_price = self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - self.current_price * norm.cdf(-d1)

        return call_price, put_price

    def calculate_greeks(self):
        d1, d2 = self.calculate_d1_d2()

        # Greeks for call option
        c_delta = norm.cdf(d1)
        c_theta = -(self.current_price * self.volatility * norm.pdf(d1)) / (2 * np.sqrt(self.time_to_maturity)) - self.interest_rate * self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)
        c_rho = self.strike * self.time_to_maturity * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)

        # Greeks for put option
        p_delta = norm.cdf(d1) - 1
        p_theta = -(self.current_price * self.volatility * norm.pdf(d1)) / (2 * np.sqrt(self.time_to_maturity)) + self.interest_rate * self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2)
        p_rho = -self.strike * self.time_to_maturity * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2)
      

        # Common Greeks for both calls and puts
        gamma = norm.pdf(d1) / (self.current_price * self.volatility * np.sqrt(self.time_to_maturity))
        vega = self.current_price * np.sqrt(self.time_to_maturity) * norm.pdf(d1) / 100

        return c_delta, p_delta, gamma, c_theta, p_theta, vega, c_rho, p_rho


col1, col2, col3 = st.columns([1,1.5,1], gap="large")

with col1:
    st.header("Black-Scholes Model Inputs")
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()
c_delta, p_delta, gamma, c_theta, p_theta, vega, c_rho, p_rho = bs_model.calculate_greeks()

with col2:
    col11, col12 = st.columns([1,1], gap="small")
    with col11:
        # Call Option Header with green background
        st.markdown("""
        <div style="background-color: #0a5e2f; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="color: white; text-align: center; margin: 0;">Call Option</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Call Price", f"{call_price:.2f}")
        st.metric("Delta", f"{c_delta:.2f}")
        st.metric("Gamma", f"{gamma:.2f}")
        st.metric("Theta", f"{c_theta:.2f}")
        st.metric("Vega", f"{vega:.2f}")
        st.metric("Rho", f"{c_rho:.2f}")

    with col12:
        # Put Option Header with red background
        st.markdown("""
        <div style="background-color: #b30000; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="color: white; text-align: center; margin: 0;">Put Option</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Put Price", f"{put_price:.2f}")
        st.metric("Delta", f"{p_delta:.2f}")
        st.metric("Gamma", f"{gamma:.2f}")
        st.metric("Theta", f"{p_theta:.2f}")
        st.metric("Vega", f"{vega:.2f}")
        st.metric("Rho", f"{p_rho:.2f}")

    
    

    
    