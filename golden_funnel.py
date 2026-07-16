import sqlite3, requests, json,pprint
from pathlib import Path

DB_PATH = Path(__file__).parent / "CS2-Skins.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
query = '''
SELECT skin_name,min_float,max_float,collection, rarity, COUNT(*) as outcome_count
FROM skins
GROUP BY collection, rarity
HAVING outcome_count = 1
'''
target_skins = cursor.execute(query).fetchall()
ladder = {
    "rarity_ancient_weapon": "rarity_legendary_weapon",
    "rarity_legendary_weapon" :"rarity_mythical_weapon",
    "rarity_mythical_weapon":"rarity_rare_weapon",
    "rarity_rare_weapon":"rarity_uncommon_weapon",
    "rarity_uncommon_weapon":"rarity_common_weapon",
    
}

def fetch_golden_funnels():
    verified_funnels = []  # This is your master list

    for target_skin in target_skins:
        target_name = target_skin[0]
        target_min = target_skin[1]
        target_max = target_skin[2]
        currect_collection = target_skin[3]
        input_rarity = ladder.get(target_skin[4])

        if not input_rarity:
            continue

        # Find ALL skins that could be anchors for THIS target
        search_query = "SELECT skin_name FROM skins WHERE rarity = ? and collection = ?"
        possible_anchors = cursor.execute(search_query, (input_rarity, currect_collection)).fetchall()

        if possible_anchors:
            # Create a FRESH dictionary for THIS specific funnel
            funnel_entry = {
                "target_name": target_name,
                "target_min": target_min,
                "target_max": target_max,
                "collection": currect_collection,
                "rarity": target_skin[4],
                "potential_anchors": [row[0] for row in possible_anchors] # Clean list of names
            }
            verified_funnels.append(funnel_entry)
            
    return verified_funnels

