"""
Black-Scholes Pricer & Greeks Dashboard
========================================
Interactive Streamlit app for European option pricing and Greek analysis.

Run with:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import bs as bs


# ── Page config ──
st.set_page_config(
    page_title="Black-Scholes Pricer",
    page_icon="📈",
    layout="wide",
)

st.title("Black-Scholes Pricer & Greeks Dashboard")
st.markdown("European option pricing with analytical Greeks under the Black-Scholes framework.")


# ══════════════════════════════════════════════════
# SIDEBAR: INPUT PARAMETERS
# ══════════════════════════════════════════════════

st.sidebar.header("Option Parameters")

S = st.sidebar.number_input("Spot Price (S)", value=100.0, min_value=0.01, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.01, step=1.0)
T = st.sidebar.number_input("Time to Expiry (years)", value=1.0, min_value=0.01, max_value=10.0, step=0.1)
r = st.sidebar.number_input("Risk-Free Rate", value=0.05, min_value=-0.05, max_value=0.30, step=0.005, format="%.3f")
vol = st.sidebar.number_input("Volatility (σ)", value=0.20, min_value=0.01, max_value=2.0, step=0.01, format="%.2f")
q = st.sidebar.number_input("Dividend Yield (q)", value=0.0, min_value=0.0, max_value=0.20, step=0.005, format="%.3f")

option_type = st.sidebar.radio("Option Type", ["call", "put"])

