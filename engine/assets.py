# assets.py
# Aidan Richer

import pandas as pd

def default_liquidity_profile():
    data = [
        # bucket,                           market_value (CAD),   days_to_cash, stress_loss_pct, available
        ["Cash & Short-Term Bonds",          9_000_000_000,        0,            0.00,      True],
        ["Public Equities [T+1]",           35_000_000_000,        1,            0.15,      True],
        ["Public Credit [T+5]",             20_000_000_000,        5,            0.08,      True],
        ["Real Estate [T+30]",              16_000_000_000,       30,            0.20,      True],
        ["Infrastructure [T+90]",           25_000_000_000,       90,            0.25,      False],
        ["Private Equity [Locked]",         35_000_000_000,      365,            0.30,      False],
    ]

    return pd.DataFrame(
        data,
        columns=[
            "bucket",
            "market_value",
            "days_to_cash",
            "stress_loss_pct",
            "available",
        ],
    )

def total_fund_value(profile):
    return profile["market_value"].sum()