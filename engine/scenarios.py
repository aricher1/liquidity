def build_scenario(redemption_rate, freeze_buckets=None):
    if freeze_buckets is None:
        freeze_buckets = []

    return {
        "redemption_rate": redemption_rate,
        "freeze_buckets": freeze_buckets
    }