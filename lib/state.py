import streamlit as st

SELECTED_FUNNEL_KEY = "selected_funnel"


def set_selected_funnel(anchor_name: str, target_name: str) -> None:
    st.session_state[SELECTED_FUNNEL_KEY] = {
        "anchor_name": anchor_name,
        "target_name": target_name,
    }


def get_selected_funnel() -> dict | None:
    return st.session_state.get(SELECTED_FUNNEL_KEY)


def funnel_signature(selected: dict | None) -> str:
    if not selected:
        return "none"
    return f"{selected['anchor_name']}||{selected['target_name']}"
