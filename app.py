# =================================================================================================================================================== #
#  Author: Aidan Richer
#
#   Liquidity Stress Engine
#
#   This is a lightweight, simplified interactive liquidity stress testing tool used to assess whether a fund can meet redemption requirements 
#   under a range of market stress scenarios, including equity drawdowns, credit spread shocks, FX movements, and elevated redemption activity. 
#   Liquidity is modeled at the bucket level with assumed liquidation timelines and stress impacts applied to market values and cash demands. 
# 
#   Note: Model assumptions are illustrative and intentionally simplified. They are not calibrated to any specific fund, strategy, or market
#         environment, and should not be interpreted as precise or predictive estimates.
# =================================================================================================================================================== #

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from engine.assets import default_liquidity_profile
from engine.liquidity import run_waterfall, apply_stress
from engine.metrics import liquidity_metrics
from engine.assumptions import ASSUMPTIONS
from engine.scenario_translation import translate_scenario
from engine.utils import (DARK_BG, CARD_BG, TEXT_MAIN, TEXT_MUTED, GREEN, RED, BORDER, fmt_bn, color_days, style_cash_used, style_remaining, inject_global_css,)


st.set_page_config(page_title="Liquidity Stress Engine", layout = "wide", initial_sidebar_state = "expanded",)
inject_global_css(st)

st.sidebar.markdown(f"<h3 style='color:{TEXT_MAIN}'>Stress Inputs</h3>", unsafe_allow_html = True)

equity = st.sidebar.slider("Equity Drawdown", 0.0, 0.99, 0.0, 0.01)
credit = st.sidebar.slider("Credit Shock", 0.0, 0.99, 0.0, 0.01)
fx = st.sidebar.slider("FX Shock", 0.0, 0.99, 0.0, 0.01)
redemption = st.sidebar.slider("Fund Redemption", 0.0, 0.99, 0.0, 0.01)
freeze_cash = st.sidebar.checkbox("Freeze Cash & ST Bonds")
freeze_t1 = st.sidebar.checkbox("Freeze Public Equities [T+1]")
freeze_t5 = st.sidebar.checkbox("Freeze Public Credit [T+5]")
freeze_t30 = st.sidebar.checkbox("Freeze Real Estate [T+30]")
freeze_t90 = st.sidebar.checkbox("Freeze Infrastructure [T+90]")

profile = default_liquidity_profile()

if freeze_cash:
    profile.loc[profile["bucket"] == "Cash & Short-Term Bonds", "available"] = False
if freeze_t1:
    profile.loc[profile["bucket"] == "Public Equities [T+1]", "available"] = False
if freeze_t5:
    profile.loc[profile["bucket"] == "Public Credit [T+5]", "available"] = False
if freeze_t30:
    profile.loc[profile["bucket"] == "Real Estate [T+30]", "available"] = False
if freeze_t90:
    profile.loc[profile["bucket"] == "Infrastructure [T+90]", "available"] = False

scenario = {"equity_drawdown": -equity, "credit_shock": -credit, "fx_shock": -fx, "redemption": redemption,}
stressed_profile, liquidity_demand = translate_scenario(profile = profile, scenario = scenario, assumptions = ASSUMPTIONS,)
stressed_profile = apply_stress(stressed_profile)
waterfall, summary = run_waterfall(stressed_profile = stressed_profile, cash_required = liquidity_demand,)
metrics = liquidity_metrics(summary)

status = "BREACH" if metrics["breach"] else "PASS"
status_color = RED if metrics["breach"] else GREEN

c1, c2, c3, c4 = st.columns(4)

def card(col, title, value, color=TEXT_MAIN):
    col.markdown(
        f"""
        <div style="
            background:{CARD_BG};
            border:1px solid {BORDER};
            padding:12px;
        ">
            <div style="color:{TEXT_MUTED}; font-size:12px;">{title}</div>
            <div style="font-size:20px; font-weight:600; color:{color};">{value}</div>
        </div>
        """,
        unsafe_allow_html = True,
    )

card(c1, "Liquidity Status", status, status_color)
card(c2, "Liquidity Coverage", f"{metrics['liquidity_coverage']:.2f}x")
card(c3, "Days to Liquidity", metrics["days_to_liquidity"])
card(c4, "Total Fund Value", fmt_bn(profile["market_value"].sum()))

st.markdown(
    f"""
    <div class="scenario-card">
        <div class="label">Scenario</div>
        <div class="item">Equity: {scenario['equity_drawdown']:.0%}</div>
        <div class="item">Credit: {scenario['credit_shock']:.0%}</div>
        <div class="item">FX: {scenario['fx_shock']:.0%}</div>
        <div class="item">Redemption: {scenario['redemption']:.0%}</div>
    </div>
    """,
    unsafe_allow_html = True,
)

st.markdown(f"<h3 style='color:{TEXT_MAIN}'>Liquidity Waterfall</h3>", unsafe_allow_html=True)

wf = waterfall.copy().rename(columns = {"bucket": "Asset Bucket", "stressed_value": "Stressed Value", "cash_used": "Cash Used", "remaining_value": "Remaining Value", "days_to_cash": "Days to Cash",})

def row_style(row):
    return [
        style_remaining(row[col], row["Cash Used"]) if col == "Remaining Value" else ""
        for col in row.index
    ]

styled = (
    wf[["Asset Bucket", "Stressed Value", "Cash Used", "Remaining Value", "Days to Cash"]]
    .style
    .apply(row_style, axis = 1)
    .applymap(style_cash_used, subset = ["Cash Used"])
    .applymap(color_days, subset = ["Days to Cash"])
    .format({"Stressed Value": fmt_bn, "Cash Used": fmt_bn, "Remaining Value": fmt_bn,})
    .set_properties(**{"background-color": CARD_BG, "border-bottom": f"1px solid {BORDER}",})
)

st.dataframe(styled, use_container_width = True)

spacer_left, col1, col2, spacer_right = st.columns([1, 3, 3, 1])

with col1:
    fig1, ax1 = plt.subplots(figsize = (5, 3))
    fig1.patch.set_facecolor(DARK_BG)
    fig1.tight_layout(pad = 2)

    ax1.set_facecolor(CARD_BG)
    ax1.tick_params(colors = TEXT_MUTED, labelsize = 9)
    ax1.title.set_color(TEXT_MAIN)

    for spine in ax1.spines.values():
        spine.set_color(BORDER)

    ax1.bar(
        ["Cash Required", "Cash Raised"],
        [metrics["cash_required"] / 1e9, metrics["cash_raised"] / 1e9,],
        color=[RED, GREEN],
    )

    ax1.set_title("Liquidity Coverage", fontsize = 10)
    ax1.set_ylabel("CAD (billions)", fontsize = 9, color = TEXT_MUTED)

    st.pyplot(fig1, use_container_width = False)

with col2:
    wf_sorted = waterfall.sort_values("days_to_cash")

    fig2, ax2 = plt.subplots(figsize = (4, 3))
    fig2.patch.set_facecolor(DARK_BG)
    fig2.tight_layout(pad = 2)

    ax2.set_facecolor(CARD_BG)
    ax2.tick_params(colors = TEXT_MUTED, labelsize = 8)
    ax2.title.set_color(TEXT_MAIN)

    for spine in ax2.spines.values():
        spine.set_color(BORDER)

    ax2.barh(wf_sorted["bucket"], wf_sorted["cash_used"] / 1e9, color=GREEN,)
    ax2.set_title("Liquidity Waterfall", fontsize = 10)
    ax2.set_xlabel("CAD (billions)", fontsize = 9, color = TEXT_MUTED)

    st.pyplot(fig2, use_container_width = False)
