import pygtrie
import json
import csv
# import os

def create_trie(path_to_csv, trie_path):
    pokemon_trie = pygtrie.CharTrie()
    with open(path_to_csv, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            name = row[1]
            pokemon_trie[name.lower()] = name
    path_to_json = trie_path
    export_to_json(pokemon_trie, path_to_json)

def export_to_json(trie, json_path):
    data = dict(trie)
    with open(json_path, mode='w', encoding='utf-8') as file:
        try:
            json.dump(data, file)
            print("Trie successfully exported to json")
        except (IOError, TypeError) as e:
            print(f"Failed to export trie to json: {e}")

def import_trie(json_path):
    with open(json_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    trie = pygtrie.CharTrie(data)
    return trie