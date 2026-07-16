import json
import pprint
from pathlib import Path

from logic_engine import calculate_anchors

potential_anchors = calculate_anchors()

FILLER_PRICE = 0.5

PRICES_PATH = Path(__file__).parent / "prices.json"

with open(PRICES_PATH, "r") as file:
    raw_data = json.load(file)
    market_data = raw_data.get('items_list', {})

def get_condition_value(float_value):
    if float_value < 0.07:
        return "(Factory New)"
    elif float_value < 0.15:
        return "(Minimal Wear)"
    elif float_value < 0.38:
        return "(Field-Tested)"
    elif float_value < 0.45:
        return "(Well-Worn)"
    else:
        return "(Battle-Scarred)"
    
def get_price(name,float_value):
    condition=get_condition_value(float_value) 
    search_query = f"{name} {condition}"
    item_data = market_data.get(search_query)
    conditions = ["(Battle-Scarred)","(Well-Worn)","(Field-Tested)","(Minimal Wear)","(Factory New)"]
    if not item_data:
        for condition in conditions:
            search_query = f"{name} {condition}"
            item_data = market_data.get(search_query)
            if item_data:
                break
    
    if item_data:
        price_data = item_data.get("price")
        if "7_days" in price_data:
            volume = price_data["7_days"].get("sold", "0") # Sometimes it's a string "50"
        
            # Clean up the string (API sometimes returns "200+")
            if isinstance(volume, str):
                volume = volume.replace(",", "").replace("+", "")
                
            if int(volume) < 5: 
                return 0.0
        seven_day = price_data.get("7_days")
        thirty_day = price_data.get("30_days")
        all_time = price_data.get("all_time")
        if seven_day:
            return seven_day.get("average")
        elif thirty_day:
            return thirty_day.get("average")
        elif all_time:
            return all_time.get("average")
    return 0.0
        
def get_expected_value(target_price:float,anchor_price:float):
    total_cost = anchor_price+(9*FILLER_PRICE)
    total_revenue=target_price*0.85
    prob_revenue = total_revenue*0.1
    prob_loss = total_cost
    expected_value = prob_revenue - prob_loss
    return expected_value



def scan_opportunities():
    """Scan all potential anchors and return positive-EV trade-ups as a DataFrame."""
    import pandas as pd

    rows = []
    for anchor in potential_anchors:
        max_anchor_float = anchor.get("Max Anchor Float")
        anchor_names = anchor.get("Potential Anchors")
        target_name = anchor.get("Target Skin")
        for anchor_name in anchor_names:
            anchor_price = get_price(anchor_name, max_anchor_float)
            target_price = get_price(target_name, 0.06)
            profit = get_expected_value(target_price, anchor_price)
            condition = get_condition_value(max_anchor_float)
            if anchor_price != 0 and profit > 0:
                rows.append({
                    "anchor_name": anchor_name,
                    "anchor_price": anchor_price,
                    "anchor_condition": condition,
                    "target_name": target_name,
                    "target_price": target_price,
                    "expected_value": round(profit, 2),
                })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    for _, row in scan_opportunities().iterrows():
        print(
            f"\n+++{row['anchor_name']} of price: {row['anchor_price']} "
            f"will yield an expected value of ${row['expected_value']} each time you run it"
        )
