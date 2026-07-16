"""Run locally after updating prices.json, then commit/push the data/ folder.

Orchestrates: skin metadata refresh -> funnel discovery -> priced opportunity
scan, and writes small derived files to data/ that the Streamlit app reads.
The raw CS2-Skins.db and prices.json stay local/gitignored.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import retrievedata  # noqa: F401  (import refreshes skin metadata in CS2-Skins.db)
from golden_funnel import fetch_golden_funnels
from market_scanner import scan_opportunities

DATA_DIR = REPO_ROOT / "data"


def build_funnels_dataframe():
    import pandas as pd

    rows = []
    for funnel in fetch_golden_funnels():
        for anchor_name in funnel["potential_anchors"]:
            rows.append({
                "target_name": funnel["target_name"],
                "target_min": funnel["target_min"],
                "target_max": funnel["target_max"],
                "collection": funnel["collection"],
                "rarity": funnel["rarity"],
                "anchor_name": anchor_name,
            })
    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)

    funnels_df = build_funnels_dataframe()
    funnels_df.to_csv(DATA_DIR / "funnels.csv", index=False)

    opportunities_df = scan_opportunities()
    opportunities_df.to_csv(DATA_DIR / "opportunities.csv", index=False)

    timestamp = datetime.now(timezone.utc).isoformat()
    (DATA_DIR / "last_refreshed.txt").write_text(timestamp)

    print(f"Refreshed: {len(funnels_df)} funnel rows, {len(opportunities_df)} opportunities.")
    print(f"Timestamp: {timestamp}")


if __name__ == "__main__":
    main()
