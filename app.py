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

# Add CSS to center metric values and labels
st.markdown("""
<style>
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

with col2:
    col11, col12 = st.columns([1,1], gap="small")
    with col11:
        # Call Option Header with green background
        st.markdown("""
        <div style="background-color: #0a5e2f; padding: 3px; border-radius: 5px; margin-bottom: 20px;">
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
        <div style="background-color: #b30000; padding: 3px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="color: white; text-align: center; margin: 0;">Put Option</h2>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Put Price", f"{put_price:.2f}")
        st.metric("Delta", f"{p_delta:.2f}")
        st.metric("Gamma", f"{gamma:.2f}")
        st.metric("Theta", f"{p_theta:.2f}")
        st.metric("Vega", f"{vega:.2f}")
        st.metric("Rho", f"{p_rho:.2f}")

with col3:
    st.header("Analysis")
    
    # Analysis header with blue background
    st.markdown("""
    <div style="background-color: #0066cc; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="color: white; text-align: center; margin: 0;">Market Insights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Price Analysis
    st.subheader("Price Analysis")
    price_ratio = round(call_price / put_price, 2) if put_price > 0 else float('inf')
    price_diff = round(call_price - put_price, 2)
    
    if price_diff > 0:
        st.write(f"Call options are trading at a premium of {price_diff:.2f} over put options.")
    elif price_diff < 0:
        st.write(f"Put options are trading at a premium of {abs(price_diff):.2f} over call options.")
    else:
        st.write("Call and put options are priced equally, suggesting market neutrality.")
    
    # Greek Analysis
    st.subheader("Greek Analysis")
    
    # Delta Analysis
    st.write("**Delta Interpretation:**")
    if c_delta > 0.7:
        st.write("Call option is highly sensitive to price movement (deep in-the-money).")
    elif c_delta < 0.3:
        st.write("Call option has low sensitivity to price movement (out-of-the-money).")
    else:
        st.write("Call option has moderate sensitivity to price changes (near-the-money).")
    
    # Gamma Analysis
    st.write("**Gamma Interpretation:**")
    if gamma > 0.05:
        st.write("High gamma indicates rapidly changing delta - position requires active management.")
    else:
        st.write("Low gamma indicates stable delta - position is less sensitive to small price changes.")
    
    # Theta Analysis
    st.write("**Theta Interpretation:**")
    if c_theta < -0.1:
        st.write("Significant time decay: option is losing value quickly with time.")
    else:
        st.write("Moderate time decay: option value is relatively stable over time.")
    
    # Vega Analysis
    st.write("**Vega Interpretation:**")
    if vega > 0.2:
        st.write("High volatility sensitivity: position is greatly affected by changes in volatility.")
    else:
        st.write("Low volatility sensitivity: position is relatively stable against volatility changes.")
    
    # Trading Strategy Suggestions
    st.subheader("Potential Strategies")
    
    if current_price > strike * 1.1:
        st.write("- Consider bull call spreads to capitalize on upward momentum")
        st.write("- Long calls may be profitable but expensive")
    elif current_price < strike * 0.9:
        st.write("- Consider bear put spreads to capitalize on downward movement")
        st.write("- Long puts may be profitable but watch time decay")
    else:
        st.write("- Consider straddles or strangles to capitalize on expected volatility")
        st.write("- Iron condors may be appropriate if expecting range-bound movement")