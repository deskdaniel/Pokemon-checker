import pygtrie
import json
import csv
# import os
from config import trie_path, database_path

def create_trie():
    pokemon_trie = pygtrie.CharTrie()
    with open(database_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            number = row[0]
            name = row[1]
            types = row[2]
            abilities = row[3]
            stats = json.loads(row[4])
            bst = row[5]
            pokemon_trie[name.lower()] = [number, name, types, abilities, stats, bst]
    export_to_json(pokemon_trie)

def export_to_json(trie):
    data = dict(trie)
    with open(trie_path, mode='w', encoding='utf-8') as file:
        try:
            json.dump(data, file)
            print("Trie successfully exported to json")
        except (IOError, TypeError) as e:
            print(f"Failed to export trie to json: {e}")

def import_trie(trie_path):
    with open(trie_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    trie = pygtrie.CharTrie(data)
    return trie