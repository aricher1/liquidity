import pandas as pd

def default_liquidity_profile():
    data = [
        # bucket,           market_value, days_to_cash, stress_loss_pct, available
        ["Cash",               75.0,              0,              0.00,      True],
        ["T+1 Liquidity",     450.0,              1,              0.12,      True],
        ["T+5 Liquidity",     300.0,              5,              0.06,      True],
        ["T+30 Liquidity",    125.0,             30,              0.10,      True],
        ["Locked Capital",     50.0,            365,              0.25,      False],
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