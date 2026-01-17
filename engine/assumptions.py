# =================================================================================================================================================== #
# Author: Aidan Richer
#
#   This file defines centralized stress and shock assumptions used across the liquidity and risk simulation framework.
#   The purpose is to parameterize how different macro or market events translate into asset-level losses and liquidity demands in a simplified way.
#
#
#    Assumptions Explanation:
#       bucket
#           - identifies which asset bucket from the liquidity profile is impacted
#           - used to map shocks directly to portfolio rows
#
#       pass_through
#           - proportion of the theoretical shock that actually impacts the asset value
#           - allows partial transmission instead of assuming full exposure
#
#       liquidity_demand_pct
#           - percentage of the bucket’s market value that must be raised as cash
#           - represents margin calls, collateral posting, or investor withdrawals, arbitrarily decided for simplicity
#
#       type
#           - categorizes the shock when it is not asset-based
#           - "direct_liability" indicates an external cash outflow not tied to asset liquidation
# =================================================================================================================================================== #

ASSUMPTIONS = {
    "equity_drawdown": {
        "bucket": "Public Equities [T+1]",
        "pass_through": 1.0,
        "liquidity_demand_pct": 0.10
    },
    "credit_shock": {
        "bucket": "Public Credit [T+5]",
        "pass_through": 0.8,
        "liquidity_demand_pct": 0.05
    },
    "fx_shock": {
        "bucket": "Cash & Short-Term Bonds",
        "pass_through": 0.5,
        "liquidity_demand_pct": 0.00
    },
    "redemption": {
        "type": "direct_liability"
    }
}
