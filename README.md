# liquidity

## Repository Layout

```text

.
├── engine/
│   ├── assets.py
│   ├── assumptions.py
│   ├── liquidity.py
│   ├── metrics.py
│   ├── scenario_translation.py
│   └── utils.py
├── app.py
├── README.md
├── requirements.txt
└── runtime.txt

```

## Description

This repository models portfolio liquidity under a range of stress scenarios. It applies scenario-level shocks to a hypothetical portfolio, translates those shocks into asset-level valuation impacts and cash requirements, and simulates the process of raising liquidity through a simplified liquidation waterfall.

The framework is designed to assess whether a fund can meet redemption requirements under stressed conditions, including equity drawdowns, credit spread shocks, FX movements, and elevated redemption activity. Liquidity is modeled at an aggregated bucket level, with assumed liquidation timelines and stress impacts applied to market values and cash demands.

All model assumptions are illustrative and intentionally simplified. They are not calibrated to any specific fund, strategy, or market environment and should not be interpreted as precise, predictive, or executable liquidity estimates.


## Usage Example

A usage example will be added here once the main script is finalized.