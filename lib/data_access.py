from pathlib import Path

import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


@st.cache_data
def load_opportunities() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "opportunities.csv")


@st.cache_data
def load_funnels() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "funnels.csv")


@st.cache_data
def load_last_refreshed() -> str:
    return (DATA_DIR / "last_refreshed.txt").read_text().strip()
