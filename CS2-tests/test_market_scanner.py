from market_scanner import scan_opportunities

EXPECTED_COLUMNS = {
    "anchor_name", "anchor_price", "anchor_condition",
    "target_name", "target_price", "expected_value",
}


def test_scan_opportunities_columns_and_positivity():
    df = scan_opportunities()
    assert EXPECTED_COLUMNS.issubset(df.columns)
    if not df.empty:
        assert (df["expected_value"] > 0).all()
        assert (df["anchor_price"] > 0).all()
