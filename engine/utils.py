# =================================================================================================================================================== #
#  Author: Aidan Richer
#
# contains the colour palette, formatting helpers, table styling, and global CSS for our app
# =================================================================================================================================================== #

# colours used
DARK_BG = "#0f1115"     # charcoal black
CARD_BG = "#151922"     # dark slate
TEXT_MAIN = "#e6e6e6"   # light grey
TEXT_MUTED = "#9aa0a6"  # slate grey
GREEN = "#2ecc71"       # green
RED = "#e74c3c"         # red
AMBER = "#f1c40f"       # golden yellow
BORDER = "#2a2f38"      # dark blue/grey


# helper functions
def fmt_bn(x):
    """
    Function to format a number as billions
    """
    try:
        return f"${x / 1e9:,.2f} bn"
    except Exception:
        return x


def color_days(val):
    """
    Function to convert color days to cash:
        - green: immediate liquidity
        - amber: short-term
        - red: long-dated
    """
    if val <= 1:
        return f"color:{GREEN}; font-weight:600"
    elif val <= 30:
        return f"color:#b26a00"
    return f"color:#b42318; font-weight:600"


def style_cash_used(val):
    """
    Function to change colour if cash used:
        - green if bucket contributes liquidity
        - muted otherwise
    """
    if val > 0:
        return f"color:{GREEN}; font-weight:600"
    return f"color:{TEXT_MUTED}"


def style_remaining(val, cash_used):
    """
    Function to change colour for remaining value:
        - red if liquidity was drawn from bucket
        - normal otherwise
    """
    if cash_used > 0:
        return f"color:{RED}; font-weight:600"
    return f"color:{TEXT_MAIN}"


def inject_global_css(st):
    """
    Function to inject our global dark-theme CSS into Streamlit
    """
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {DARK_BG};
            color: {TEXT_MAIN};
        }}

        .stApp {{
            background-color: {DARK_BG};
        }}

        .stDataFrame td {{
            font-size: 14px !important;
        }}

        .stDataFrame th {{
            font-size: 15px !important;
            font-weight: 600;
        }}

        .scenario-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 10px 14px;
            margin-top: 8px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 18px;
            font-size: 14px;
        }}

        .scenario-card .label {{
            color: {TEXT_MAIN};
            font-weight: 600;
        }}

        .scenario-card .item {{
            color: {TEXT_MUTED};
            white-space: nowrap;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
