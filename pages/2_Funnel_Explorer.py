import streamlit as st

from lib.data_access import load_funnels, load_last_refreshed
from lib.state import funnel_signature, get_selected_funnel, set_selected_funnel

st.set_page_config(page_title="Funnel Explorer", page_icon="🧭", layout="wide")
st.title("Funnel Explorer")
st.caption(f"Data as of {load_last_refreshed()}")

df = load_funnels()

incoming = get_selected_funnel()
sig = funnel_signature(incoming)

default_collections = []
default_search = ""
if incoming:
    match = df[df["target_name"] == incoming["target_name"]]
    if not match.empty:
        default_collections = sorted(match["collection"].unique())
        default_search = incoming["target_name"]
    st.info(
        f"Showing funnels for **{incoming['target_name']}** "
        f"(arrived from Opportunities: {incoming['anchor_name']} → {incoming['target_name']})."
    )

collections = sorted(df["collection"].unique())
selected_collections = st.multiselect(
    "Collection", collections, default=default_collections, key=f"collections_{sig}"
)

filtered = df if not selected_collections else df[df["collection"].isin(selected_collections)]

search = st.text_input("Search target or anchor skin name", value=default_search, key=f"search_{sig}")
if search:
    mask = filtered["target_name"].str.contains(search, case=False, na=False) | filtered[
        "anchor_name"
    ].str.contains(search, case=False, na=False)
    filtered = filtered[mask]

filtered = filtered.reset_index(drop=True)
event = st.dataframe(
    filtered,
    width="stretch",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="funnels_table",
)
st.caption(f"{len(filtered)} of {len(df)} funnel pairs shown. Select a row to test it in the Risk Simulator.")

selected_rows = event.get("selection", {}).get("rows", []) if event else []
if selected_rows:
    row = filtered.iloc[selected_rows[0]]
    st.info(f"Selected: **{row.anchor_name} → {row.target_name}**")
    if st.button("Test this funnel in Risk Simulator →", type="primary"):
        set_selected_funnel(row.anchor_name, row.target_name)
        st.switch_page("pages/3_Risk_Simulator.py")
