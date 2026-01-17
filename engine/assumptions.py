# assumptions.py
# Aidan Richer

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
