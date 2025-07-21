import os

root_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root_dir, "data")
database_path = os.path.join(data_dir, "database.csv")
types_path = os.path.join(data_dir, "types_chart.csv")
trie_path = os.path.join(data_dir, "pokemon_trie.json")

damage_altering_abilities = {"Dry Skin": {"Fire": 1.25, "Water": 0},
                            "Earth Eater": {"Ground": 0},
                            "Filter": {"condition": "super effective", "multiplier": 0.75},
                            "Flash Fire": {"Fire": 0},
                            "Fluffy": {"Fire": 2},
                            "Heatproof": {"Fire": 0.5},
                            "Levitate": {"Ground": 0},
                            "Lightning Rod": {"Electric": 0},
                            "Motor Drive": {"Electric": 0},
                            "Prism Armor": {"condition": "super effective", "multiplier": 0.75},
                            "Purifying Salt": {"Ghost": 0.5},
                            "Sap Sipper": {"Grass": 0},
                            "Solid Rock": {"condition": "super effective", "multiplier": 0.75},
                            "Storm Drainr": {"Water": 0},
                            "Thick Fat": {"Fire": 0.5, "Ice": 0.5},
                            "Volt Absorb": {"Electric": 0},
                            "Water Absorb": {"Water": 0},
                            "Water Bubble": {"Fire": 0.5},
                            "Well Baked Body": {"Fire": 0},
                            "Wonder Guard": {"condition": "not super effective", "multiplier": 0},
                            }