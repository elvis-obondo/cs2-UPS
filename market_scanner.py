import json
import pprint
from logic_engine import calculate_anchors

potential_anchors = calculate_anchors()

FILLER_PRICE = 0.5

with open("CS2/prices.json","r") as file:
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



for anchor in potential_anchors:
    max_anchor_float = anchor.get("Max Anchor Float")
    anchor_names = anchor.get("Potential Anchors")
    target_name = anchor.get("Target Skin")
    for anchor_name in anchor_names:
        anchor_price = get_price(anchor_name,max_anchor_float)
        target_price = get_price(target_name, 0.06)
        profit = get_expected_value(target_price,anchor_price)
        condition = get_condition_value(max_anchor_float)
        if anchor_price!=0:
            if profit>0:
                print(f"\n+++{anchor_name} of price: {anchor_price} will yield an expected value of ${round(profit,2)} each time you run it")
            
            

