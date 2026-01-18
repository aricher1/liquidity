# =================================================================================================================================================== #
# Author: Aidan Richer
#
#   This file constructs a hypothetical institutional-style portfolio made up of common asset classes with different liquidity and risk profiles.
#   The purpose is to simulate fund-level liquidity, stress behaviour, and total portfolio value using simplified but realistic assumptions.
#
#
#    Data Explanation:
#       bucket
#           - name of the asset class
#           - also encodes liquidity assumptions (T+1, T+30, Locked)
#
#       market_value
#           - total market value of the assets in bucket in CAD
#           - used for portfolio weighting and total fund size calculations
#
#       days_to_cash
#           - estimated number of days required to convert the asset into usable cash
#           - same as the number of days in the liquidity assumption
#
#       stress_loss_pct
#           - expected percentage loss if the asset must be liquidated under stress
#           - these are non-perfect assumptions, and are arbitraility picked for the simplicity of this project
#
#       available
#           - boolean flag indicating if the capital is usable for near-term needs
#           - for simplicity, we assume liquidity is only accessible within the next 30 days, and exclude T+90 and Locked
#
# =================================================================================================================================================== #

import pandas as pd

def default_liquidity_profile():
    """
    - Construct an arbitrary portfolio of such asset classes
    - Returns a pd data frame of the portfolio
    """

    data = [
        # bucket,                       market_value (CAD),   days_to_cash, stress_loss_pct, available
        ["Cash & Short-Term Bonds",          9_000_000_000,        0,            0.00,      True],
        ["Public Equities [T+1]",           35_000_000_000,        1,            0.15,      True],
        ["Public Credit [T+5]",             20_000_000_000,        5,            0.08,      True],
        ["Real Estate [T+30]",              16_000_000_000,       30,            0.20,      True],
        ["Infrastructure [T+90]",           25_000_000_000,       90,            0.25,      False],
        ["Private Equity [Locked]",         35_000_000_000,      365,            0.30,      False],
    ]

    # return pd dataframe
    return pd.DataFrame(data, columns=["bucket", "market_value", "days_to_cash", "stress_loss_pct", "available",],)

def total_fund_value(profile):
    """
    Calculate the total portfolio value by summing the market_value column
    """
    return profile["market_value"].sum()