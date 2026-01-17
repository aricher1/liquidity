# metrics.py
# Aidan Richer

def liquidity_metrics(summary):
    cash_required = summary["cash_required"]
    cash_raised = summary["cash_raised"]
    shortfall = summary["shortfall"]

    coverage_ratio = cash_raised / cash_required if cash_required > 0 else 1.0
    shortfall_pct = shortfall / cash_required if cash_required > 0 else 0.0

    return {
        "cash_required": cash_required,
        "cash_raised": cash_raised,
        "liquidity_coverage": coverage_ratio,
        "shortfall_pct": shortfall_pct,
        "days_to_liquidity": summary["days_to_liquidity"],
        "breach": summary["breach"]
    }
