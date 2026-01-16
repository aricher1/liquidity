import pandas as pd

def apply_stress(profile):
    stressed = profile.copy()
    stressed["stressed_value"] = stressed["market_value"] * (1 - stressed["stress_loss_pct"])
    return stressed

def run_waterfall(stressed_profile, cash_required):
    rows = []
    remaining_need = cash_required
    days_to_liquidity = 0
    cash_raised = 0.0

    profile = stressed_profile.sort_values("days_to_cash")

    for _, row in profile.iterrows():
        usable = 0.0

        if row["available"] and remaining_need > 0:
            usable = min(row["stressed_value"], remaining_need)

        remaining_value = row["stressed_value"] - usable

        if usable > 0:
            days_to_liquidity = max(days_to_liquidity, row["days_to_cash"])
            cash_raised += usable
            remaining_need -= usable

        rows.append({
            "bucket": row["bucket"],
            "stressed_value": row["stressed_value"],
            "cash_used": usable,
            "remaining_value": remaining_value,
            "days_to_cash": row["days_to_cash"]
        })

    waterfall = pd.DataFrame(rows)

    return waterfall, {
        "cash_required": cash_required,
        "cash_raised": cash_raised,
        "shortfall": max(0.0, remaining_need),
        "days_to_liquidity": days_to_liquidity,
        "breach": remaining_need > 0
    }

def run_liquidity_stress(profile, redemption_rate):
    stressed = apply_stress(profile)
    total_stressed_value = stressed["stressed_value"].sum()
    cash_required = redemption_rate * total_stressed_value
    return run_waterfall(stressed, cash_required)
