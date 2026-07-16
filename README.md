# CS2 Asset Arbitrage & Risk Engine

A research tool designed to identify structural pricing inefficiencies in the Counter-Strike 2 (CS2) skin market following the Universal Float Scaling (UFS) update.
# The Thesis
Traditional market pricing in CS2 relies on categorical labels (e.g., "Minimal Wear," "Field-Tested"). 
However, the underlying game logic calculates asset "wear" using a raw fractional value (Float). 
By leveraging the Float Bridge strategy, this engine identifies specific asset combinations where the cost of inputs is mathematically mispriced relative to the expected value (EV) of the output.
# Features
Universal Float Scaling (UFS) Logic: A dedicated module that calculates the precise "Max Anchor Float" required to force a high-tier condition outcome using a 1-anchor, 9-filler strategy.
Real-Time Market Scanner: Parses large-scale JSON datasets to bridge the gap between theoretical float math and current market prices.
Expected Value (EV) Engine: A risk-assessment module that calculates the true profitability of a trade-up by factoring in:
• 15% Steam Market Transaction Tax.
• Probability-weighted outcomes (10% success rate modeling).
• Volume filters to remove "ghost" or illiquid listings.
Variance Simulator: A Monte Carlo-style simulation tool to visualize the equity curve and drawdowns associated with low-win-rate, high-payout trading systems.
# Methodology
Extraction: Scrapes/Parses global price and volume data.
Analysis: Runs every skin through the logic_engine to find the "Float Bridge" threshold.
Validation: Filters candidates based on 7-day sales volume and 30-day price averages to ensure data integrity.
Verdict: Outputs a list of high-conviction trade-ups sorted by Positive Expected Value.
# Tech Stack
Python 3.12
JSON Data Modeling
Monte Carlo Variance Simulation

