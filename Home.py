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

**Pages** — designed to be worked in order:
1. **Opportunities** — current positive expected-value trade-ups, ranked and filterable.
2. **Funnel Explorer** — select a row in Opportunities to jump here and see every anchor
   that can be traded up into that same target skin.
3. **Risk Simulator** — select a row in Funnel Explorer to test that specific funnel here:
   the distribution of outcomes across many simulated attempts (variance, drawdown, risk of ruin).
"""
)
