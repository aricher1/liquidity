from engine.assets import default_liquidity_profile
from engine.scenarios import build_scenario
from engine.liquidity import run_liquidity_stress
from engine.metrics import liquidity_metrics


def main():
    profile = default_liquidity_profile()

    scenario = build_scenario(
        redemption_rate=0.10,
        freeze_buckets=[]
        # example:
        # freeze_buckets=["T+1 Liquidity", "T+5 Liquidity"]
    )

    if scenario["freeze_buckets"]:
        profile.loc[
            profile["bucket"].isin(scenario["freeze_buckets"]),
            "available"
        ] = False

    waterfall, summary = run_liquidity_stress(
        profile=profile,
        redemption_rate=scenario["redemption_rate"]
    )

    metrics = liquidity_metrics(summary)

    print("\n=== Liquidity Stress Results ===\n")
    print("Scenario:")
    print(scenario)

    print("\nHeadline Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nLiquidity Waterfall:")
    print(waterfall)


if __name__ == "__main__":
    main()
