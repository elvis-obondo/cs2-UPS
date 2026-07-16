import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from lib.data_access import load_last_refreshed, load_opportunities
from monte_carlo import run_batch_simulation

# Mirrors market_scanner.py's cost/revenue assumptions. Not imported directly
# because that module queries CS2-Skins.db and opens prices.json at import
# time -- fine for the local offline refresh, not available in the deployed app.
FILLER_PRICE = 0.5
FILLER_COUNT = 9
STEAM_TAX = 0.15
DEFAULT_WIN_CHANCE_PCT = 10  # matches market_scanner's documented success-rate model

st.set_page_config(page_title="Risk Simulator", page_icon="🎲", layout="wide")
st.title("Risk Simulator")
st.caption(f"Data as of {load_last_refreshed()}")

st.markdown(
    """
A golden funnel guarantees *which* skin you get, but not that the market price
holds steady, and any single attempt can still cost you money if float or price
assumptions are slightly off. This simulates many independent attempts so you
can see the *spread* of outcomes, not just the average expected value.

Set win chance to 100% to model a true golden funnel (deterministic payout each
attempt); use a lower value to stress-test what happens if the assumptions
underneath a funnel don't hold every time.
"""
)

opportunities = load_opportunities()

st.subheader("Load a real opportunity")
if opportunities.empty:
    choice = "— manual —"
    st.info("No priced opportunities available — configure the simulator manually below.")
else:
    labels = [
        f"{row.anchor_name} → {row.target_name}  (EV ${row.expected_value:.2f})"
        for row in opportunities.itertuples()
    ]
    choice = st.selectbox("Preload cost/payout from Opportunities", ["— manual —"] + labels)

if choice == "— manual —":
    selected = None
    default_cost, default_payout = 7.50, 85.00
else:
    selected = opportunities.iloc[labels.index(choice)]
    default_cost = round(float(selected.anchor_price) + FILLER_COUNT * FILLER_PRICE, 2)
    default_payout = round(float(selected.target_price) * (1 - STEAM_TAX), 2)
    st.caption(
        f"Preloaded **{selected.anchor_name}** ({selected.anchor_condition}) → "
        f"**{selected.target_name}**. Cost/attempt = anchor price (${selected.anchor_price:.2f}) "
        f"+ {FILLER_COUNT} fillers at ${FILLER_PRICE:.2f}. Payout = target price "
        f"(${selected.target_price:.2f}) less {STEAM_TAX:.0%} Steam Market tax."
    )

col1, col2, col3 = st.columns(3)
with col1:
    starting_bankroll = st.number_input(
        "Starting bankroll ($)", min_value=0.0, value=300.0, step=10.0
    )
    cost_per_try = st.number_input(
        "Cost per attempt ($)", min_value=0.01, value=default_cost, step=0.50, key=f"cost_{choice}"
    )
with col2:
    win_payout = st.number_input(
        "Payout on a win ($)", min_value=0.0, value=default_payout, step=1.0, key=f"payout_{choice}"
    )
    win_chance_pct = st.slider(
        "Win chance (%)", min_value=0, max_value=100, value=DEFAULT_WIN_CHANCE_PCT
    )
with col3:
    total_attempts = st.slider("Number of attempts", min_value=1, max_value=200, value=30)
    n_trials = st.select_slider(
        "Simulated trials", options=[100, 500, 1000, 2000, 5000], value=1000
    )

seed = st.number_input("Random seed", min_value=0, value=42, step=1)

history = run_batch_simulation(
    n_trials=n_trials,
    starting_bankroll=starting_bankroll,
    cost_per_try=cost_per_try,
    win_payout=win_payout,
    win_chance=win_chance_pct / 100,
    total_attempts=total_attempts,
    seed=seed,
)

final_balances = history[:, -1]
running_max = np.maximum.accumulate(history, axis=1)
max_drawdown = (running_max - history).max(axis=1)
risk_of_ruin = (history.min(axis=1) < cost_per_try).mean()
prob_profit = (final_balances > starting_bankroll).mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Median final balance", f"${np.median(final_balances):,.2f}")
m2.metric("Probability of profit", f"{prob_profit:.0%}")
m3.metric(
    "Risk of ruin",
    f"{risk_of_ruin:.0%}",
    help="Share of simulated runs where the bankroll dropped below the cost of the next attempt at some point.",
)
m4.metric("Median max drawdown", f"${np.median(max_drawdown):,.2f}")

percentiles = np.percentile(history, [10, 50, 90], axis=0)
band_df = pd.DataFrame(
    {
        "attempt": np.arange(total_attempts + 1),
        "p10": percentiles[0],
        "p50": percentiles[1],
        "p90": percentiles[2],
    }
)

band = alt.Chart(band_df).mark_area(opacity=0.25, color="#2a78d6").encode(
    x=alt.X("attempt:Q", title="Attempt #"),
    y=alt.Y("p10:Q", title="Bankroll ($)"),
    y2="p90:Q",
)
median_line = alt.Chart(band_df).mark_line(color="#2a78d6", strokeWidth=2).encode(
    x="attempt:Q", y="p50:Q"
)
broke_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
    color="#d03b3b", strokeDash=[4, 4]
).encode(y="y:Q")

hover = alt.selection_point(fields=["attempt"], nearest=True, on="mouseover", empty=False)
hover_targets = alt.Chart(band_df).mark_point(opacity=0).encode(x="attempt:Q").add_params(hover)
hover_rule = alt.Chart(band_df).mark_rule(color="gray").encode(
    x="attempt:Q",
    opacity=alt.condition(hover, alt.value(0.4), alt.value(0)),
    tooltip=[
        alt.Tooltip("attempt:Q", title="Attempt"),
        alt.Tooltip("p10:Q", title="10th pct", format="$.2f"),
        alt.Tooltip("p50:Q", title="Median", format="$.2f"),
        alt.Tooltip("p90:Q", title="90th pct", format="$.2f"),
    ],
)

st.altair_chart(
    (band + median_line + broke_line + hover_targets + hover_rule).interactive(),
    width="stretch",
)
st.caption(
    f"Shaded band = 10th–90th percentile bankroll across {n_trials:,} simulated runs "
    "of the same strategy. Dashed red line = broke ($0)."
)

with st.expander("Percentile data"):
    st.dataframe(band_df, width="stretch", hide_index=True)
