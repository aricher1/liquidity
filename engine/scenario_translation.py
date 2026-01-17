# =================================================================================================================================================== #
# Author: Aidan Richer
#
#   This file translates high-level scenario inputs into concrete portfolio impacts.
#   The purpose is to convert abstract shocks (e.g. equity drawdown, redemption) into asset-level stress losses and total liquidity required.
#
#       translate_scenario
#           - takes a scenario dictionary and applies it to the portfolio
#           - adjusts stress losses on specific asset buckets
#           - calculates total cash that must be raised
#
# =================================================================================================================================================== #


def translate_scenario(profile, scenario, assumptions):
    """
    Function to apply the user-defined scenario and calculate the total cash that must be raised
    """
    stressed_profile = profile.copy()
    total_liquidity_demand = 0.0
    total_fund_value = profile["market_value"].sum()

    for shock, value in scenario.items():
        if shock not in assumptions:
            continue

        rule = assumptions[shock]

        if rule.get("type") == "direct_liability":
            total_liquidity_demand += abs(value) * total_fund_value
            continue

        bucket = rule["bucket"]
        pass_through = rule.get("pass_through", 1.0)
        liquidity_demand_pct = rule.get("liquidity_demand_pct", 0.0)

        # valuation impact
        stressed_profile.loc[
            stressed_profile["bucket"] == bucket,
            "stress_loss_pct"
        ] += abs(value) * pass_through

        # liquidity demand
        if liquidity_demand_pct > 0:
            bucket_value = profile.loc[
                profile["bucket"] == bucket, "market_value"
            ].values[0]

            total_liquidity_demand += liquidity_demand_pct * abs(value) * bucket_value

    return stressed_profile, total_liquidity_demand