import streamlit as st

from lib.data_access import load_funnels, load_last_refreshed

st.set_page_config(page_title="Funnel Explorer", page_icon="🧭", layout="wide")
st.title("Funnel Explorer")
st.caption(f"Data as of {load_last_refreshed()}")

df = load_funnels()

collections = sorted(df["collection"].unique())
selected_collections = st.multiselect("Collection", collections, default=[])

filtered = df if not selected_collections else df[df["collection"].isin(selected_collections)]

search = st.text_input("Search target or anchor skin name")
if search:
    mask = filtered["target_name"].str.contains(search, case=False, na=False) | filtered[
        "anchor_name"
    ].str.contains(search, case=False, na=False)
    filtered = filtered[mask]

st.dataframe(filtered, width="stretch", hide_index=True)
st.caption(f"{len(filtered)} of {len(df)} funnel pairs shown.")
