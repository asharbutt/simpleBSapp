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
import bs_model as bs


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
sigma = st.sidebar.number_input("Volatility (σ)", value=0.20, min_value=0.01, max_value=2.0, step=0.01, format="%.2f")
q = st.sidebar.number_input("Dividend Yield (q)", value=0.0, min_value=0.0, max_value=0.20, step=0.005, format="%.3f")

option_type = st.sidebar.radio("Option Type", ["call", "put"])


# ══════════════════════════════════════════════════
# PRICE & GREEKS SUMMARY
# ══════════════════════════════════════════════════

greeks = bs.all_greeks(S, K, T, r, sigma, q, option_type)

st.markdown("---")
st.subheader(f"{'Call' if option_type == 'call' else 'Put'} Option Summary")

# Display in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Price", f"${greeks['price']:.4f}")
    st.metric("Delta (Δ)", f"{greeks['delta']:.4f}")
    st.metric("Gamma (Γ)", f"{greeks['gamma']:.6f}")

with col2:
    st.metric("Vega (ν)", f"{greeks['vega']:.4f}")
    st.metric("Theta (Θ)", f"{greeks['theta']:.4f}")
    st.metric("Rho (ρ)", f"{greeks['rho']:.4f}")

with col3:
    st.metric("Vanna", f"{greeks['vanna']:.6f}")
    st.metric("Volga", f"{greeks['volga']:.6f}")
    st.metric("Charm", f"{greeks['charm']:.6f}")


# ══════════════════════════════════════════════════
# CHART 1: PRICE vs SPOT
# ══════════════════════════════════════════════════

st.markdown("---")
st.subheader("Price & Delta vs Spot")

spot_range = np.linspace(S * 0.5, S * 1.5, 200)

prices = np.array([bs.price(s, K, T, r, sigma, q, option_type) for s in spot_range])
deltas = np.array([bs.delta(s, K, T, r, sigma, q, option_type) for s in spot_range])

# Intrinsic value for reference
if option_type == "call":
    intrinsic = np.maximum(spot_range - K, 0)
else:
    intrinsic = np.maximum(K - spot_range, 0)

fig1 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Option Price vs Spot", "Delta vs Spot"),
    horizontal_spacing=0.08,
)

# Price plot
fig1.add_trace(
    go.Scatter(x=spot_range, y=prices, name="Option Price", line=dict(color="#c9a96e", width=2)),
    row=1, col=1,
)
fig1.add_trace(
    go.Scatter(x=spot_range, y=intrinsic, name="Intrinsic Value", line=dict(color="#555", width=1, dash="dash")),
    row=1, col=1,
)
fig1.add_vline(x=K, line_dash="dot", line_color="#666", row=1, col=1)

# Delta plot
fig1.add_trace(
    go.Scatter(x=spot_range, y=deltas, name="Delta", line=dict(color="#3b7dd8", width=2)),
    row=1, col=2,
)
fig1.add_vline(x=K, line_dash="dot", line_color="#666", row=1, col=2)

fig1.update_layout(
    height=400,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,17,21,1)",
    font=dict(size=11),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2),
)
fig1.update_xaxes(title_text="Spot Price", gridcolor="rgba(40,40,50,0.8)")
fig1.update_yaxes(gridcolor="rgba(40,40,50,0.8)")

st.plotly_chart(fig1, use_container_width=True)


# ══════════════════════════════════════════════════
# CHART 2: ALL GREEKS vs SPOT
# ══════════════════════════════════════════════════

st.subheader("Greeks vs Spot")

gammas = np.array([bs.gamma(s, K, T, r, sigma, q) for s in spot_range])
vegas = np.array([bs.vega(s, K, T, r, sigma, q) for s in spot_range])
thetas = np.array([bs.theta(s, K, T, r, sigma, q, option_type) for s in spot_range])
rhos = np.array([bs.rho(s, K, T, r, sigma, q, option_type) for s in spot_range])

fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Gamma vs Spot", "Vega vs Spot", "Theta vs Spot", "Rho vs Spot"),
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
)

fig2.add_trace(go.Scatter(x=spot_range, y=gammas, name="Gamma", line=dict(color="#6bba7b", width=2)), row=1, col=1)
fig2.add_trace(go.Scatter(x=spot_range, y=vegas, name="Vega", line=dict(color="#d4a843", width=2)), row=1, col=2)
fig2.add_trace(go.Scatter(x=spot_range, y=thetas, name="Theta", line=dict(color="#cc7a7a", width=2)), row=2, col=1)
fig2.add_trace(go.Scatter(x=spot_range, y=rhos, name="Rho", line=dict(color="#b07acc", width=2)), row=2, col=2)

for row in [1, 2]:
    for col in [1, 2]:
        fig2.add_vline(x=K, line_dash="dot", line_color="#666", row=row, col=col)

fig2.update_layout(
    height=600,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,17,21,1)",
    font=dict(size=11),
    showlegend=False,
)
fig2.update_xaxes(title_text="Spot Price", gridcolor="rgba(40,40,50,0.8)")
fig2.update_yaxes(gridcolor="rgba(40,40,50,0.8)")

st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════
# CHART 3: PRICE SURFACE (Spot x Vol)
# ══════════════════════════════════════════════════

st.markdown("---")
st.subheader("Price Surface: Spot × Volatility")

spots_3d = np.linspace(S * 0.6, S * 1.4, 60)
vols_3d = np.linspace(0.05, 0.60, 60)
spots_grid, vols_grid = np.meshgrid(spots_3d, vols_3d)

prices_3d = np.array([
    [bs.price(s, K, T, r, v, q, option_type) for s in spots_3d]
    for v in vols_3d
])

fig3 = go.Figure(data=[
    go.Surface(
        x=spots_grid,
        y=vols_grid,
        z=prices_3d,
        colorscale="YlOrBr",
        opacity=0.9,
        showscale=True,
        colorbar=dict(title="Price", len=0.6),
    )
])

fig3.update_layout(
    height=550,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    scene=dict(
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        zaxis_title="Option Price",
        xaxis=dict(gridcolor="rgba(40,40,50,0.8)"),
        yaxis=dict(gridcolor="rgba(40,40,50,0.8)"),
        zaxis=dict(gridcolor="rgba(40,40,50,0.8)"),
        bgcolor="rgba(17,17,21,1)",
    ),
    font=dict(size=11),
)

st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════
# CHART 4: GREEKS HEATMAP (Spot x Time)
# ══════════════════════════════════════════════════

st.subheader("Delta Heatmap: Spot × Time to Expiry")

spots_hm = np.linspace(S * 0.7, S * 1.3, 80)
times_hm = np.linspace(0.05, T * 1.5, 80)

delta_heatmap = np.array([
    [bs.delta(s, K, t, r, sigma, q, option_type) for s in spots_hm]
    for t in times_hm
])

fig4 = go.Figure(data=[
    go.Heatmap(
        x=spots_hm,
        y=times_hm,
        z=delta_heatmap,
        colorscale="RdBu",
        zmid=0.5 if option_type == "call" else -0.5,
        colorbar=dict(title="Delta"),
    )
])

fig4.update_layout(
    height=450,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,17,21,1)",
    xaxis_title="Spot Price",
    yaxis_title="Time to Expiry (years)",
    font=dict(size=11),
)

st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════
# FORMULAS (collapsible)
# ══════════════════════════════════════════════════

st.markdown("---")
with st.expander("Black-Scholes Formulas"):
    st.latex(r"C = S e^{-qT} \Phi(d_1) - K e^{-rT} \Phi(d_2)")
    st.latex(r"P = K e^{-rT} \Phi(-d_2) - S e^{-qT} \Phi(-d_1)")
    st.latex(r"d_1 = \frac{\ln(S/K) + (r - q + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}")
    st.markdown("---")
    st.markdown("**First-order Greeks:**")
    st.latex(r"\Delta_{\text{call}} = e^{-qT} \Phi(d_1), \quad \Delta_{\text{put}} = e^{-qT}[\Phi(d_1) - 1]")
    st.latex(r"\mathcal{V} = S e^{-qT} \phi(d_1) \sqrt{T}")
    st.latex(r"\rho_{\text{call}} = KT e^{-rT} \Phi(d_2)")
    st.markdown("**Second-order Greeks:**")
    st.latex(r"\Gamma = \frac{e^{-qT} \phi(d_1)}{S \sigma \sqrt{T}}")
    st.latex(r"\text{Vanna} = -e^{-qT} \phi(d_1) \frac{d_2}{\sigma}")
    st.latex(r"\text{Volga} = \mathcal{V} \cdot \frac{d_1 d_2}{\sigma}")
