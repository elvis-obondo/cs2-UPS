import sqlite3, requests, json,pprint
connection = sqlite3.connect("CS2/CS2-Skins.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS skins (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        steam_id     TEXT UNIQUE,
        skin_name    TEXT NOT NULL,
        min_float    REAL,
        max_float    REAL,
        rarity       TEXT,
        collection   TEXT
    )
""")
response = requests.get("https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json")
if response.status_code == 200:
    data = response.json()
    

    if data:
        skins = []
        query = "INSERT OR IGNORE INTO skins (steam_id,skin_name,min_float,max_float,rarity,collection) VALUES (?,?,?,?,?,?)"
        
        for skin in data:
            if skin.get("collections"):
                values = (
                    skin.get("id","unknown"),
                    skin.get("name","unknown"),
                    skin.get("min_float",0.00),
                    skin.get("max_float",1.00),
                    skin.get("rarity",{}).get("id","unknown"),
                    skin.get("collections",["unknown"])[0].get("id")
                )
            
                skins.append(values)
        print(f"There are {len(skins)} tradable skins!")
        
        cursor.executemany(query,skins)

        connection.commit()


