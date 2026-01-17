# liquidity

## Repository Layout

```text
.
├── engine/
│   ├── assets.py
│   ├── assumptions.py
│   ├── liquidity.py
│   ├── metrics.py
│   └── scenario_translation.py
├── liquidity_stress_app.py
├── README.md
├── requirements.txt
└── runtime.txt

## Description

This repository models portfolio liquidity under different stress tests. 
It applies scenario shocks to a hypothetical portfolio, translates those shocks 
into asset-level losses and cash requirements, and simulates raising liquidity 
through a simple liquidation waterfall. The model is intentionally simple. 
It is meant to test mechanics and logic, not to produce realistic or calibrated results.

## Usage Example

A usage example will be added here once the main script is finalized.
