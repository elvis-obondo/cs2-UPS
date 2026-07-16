import streamlit as st

from lib.data_access import load_last_refreshed

st.set_page_config(page_title="CS2 Float Arbitrage", page_icon="🎯", layout="wide")

st.title("CS2 Float Arbitrage")
st.caption(f"Data as of {load_last_refreshed()}")

st.markdown(
    """
This tool scans CS2 skin "trade-up" contracts for cases where mixing cheap Factory New
skins with a well-chosen anchor produces a valid float on a specific rare target skin,
at a positive expected value against current market prices.

It's published openly rather than kept private — every opportunity here is visible to
anyone who opens this page, refreshed whenever the maintainer updates market prices.

**Pages**
- **Opportunities** — current positive expected-value trade-ups, ranked and filterable.
- **Funnel Explorer** — the underlying map of which cheap anchor skins can be traded up
  into which valuable target skins.
- **Risk Simulator** — before running a real trade-up, see the distribution of outcomes
  across many simulated attempts (variance, drawdown, risk of ruin).
"""
)
