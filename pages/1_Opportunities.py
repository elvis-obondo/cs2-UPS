import streamlit as st

from lib.data_access import load_opportunities, load_last_refreshed

st.set_page_config(page_title="Opportunities", page_icon="🎯", layout="wide")
st.title("Opportunities")
st.caption(f"Data as of {load_last_refreshed()}")

df = load_opportunities()

if df.empty:
    st.info("No positive expected-value opportunities found in the current data.")
else:
    max_ev = float(df["expected_value"].max())
    ev_threshold = st.slider(
        "Minimum expected value ($)", min_value=0.0, max_value=max_ev, value=0.0, step=0.5
    )
    conditions = sorted(df["anchor_condition"].unique())
    selected_conditions = st.multiselect("Anchor condition", conditions, default=conditions)

    filtered = df[
        (df["expected_value"] >= ev_threshold) & (df["anchor_condition"].isin(selected_conditions))
    ].sort_values("expected_value", ascending=False)

    st.dataframe(filtered, width="stretch", hide_index=True)
    st.caption(f"{len(filtered)} of {len(df)} opportunities shown.")
