import pprint
import statistics

from golden_funnel import fetch_golden_funnels



def calculate_tradeup(fillers:list[float], anchor:float,t_min:float,t_max:float):
    """calculate_tradeup _summary_
        • This works well if the anchor is between 0.07 and 0.08
        • The fillers need to have factory new values. MUST BE
        lower than 0.07 for them to bring the "dirt" down
        • Works well if the target skin min = 0 and the max is <0.7

    Args:
        fillers (list[float]): Needs to be Factory New (And dirt cheap)
        anchor (float): Needs to be from target skin collection
        t_max (float): Preferably should have a very low ceiling
    """
    trade_up = fillers + [anchor]
    output_float = (statistics.mean(trade_up) * t_max - t_min) + t_min
    return output_float 


def calculate_anchors():
    funnels = fetch_golden_funnels()
    max_anchor_values = []
    fillers_sum = 0.01*9

    for funnel in funnels:
        target_max = funnel.get("target_max")
        target_min = funnel.get("target_min")
        factory_new_space = 0.06999999999 - target_min
        if factory_new_space < 0:
            continue
        target_skin_range = target_max - target_min
        # represents the total range avaialable to us
        total = (factory_new_space/target_skin_range) * 10
        anchor_value = min((total - fillers_sum),1.0)
        if 0.05 < anchor_value :

            max_anchor = {
                "Target Skin": funnel.get("target_name"),
                "Target Max" : target_max,
                "Target Min" : target_min,
                "Max Anchor Float": anchor_value,
                "Potential Anchors": funnel.get("potential_anchors")
            }
            max_anchor_values.append(max_anchor)
    return max_anchor_values
