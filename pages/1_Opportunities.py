import streamlit as st

from lib.data_access import load_opportunities, load_last_refreshed
from lib.state import set_selected_funnel

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
    ].sort_values("expected_value", ascending=False).reset_index(drop=True)

    event = st.dataframe(
        filtered,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="opportunities_table",
    )
    st.caption(f"{len(filtered)} of {len(df)} opportunities shown. Select a row to explore its funnel.")

    selected_rows = event.get("selection", {}).get("rows", []) if event else []
    if selected_rows:
        row = filtered.iloc[selected_rows[0]]
        st.info(f"Selected: **{row.anchor_name} → {row.target_name}** (EV ${row.expected_value:.2f})")
        if st.button("Explore this funnel →", type="primary"):
            set_selected_funnel(row.anchor_name, row.target_name)
            st.switch_page("pages/2_Funnel_Explorer.py")
