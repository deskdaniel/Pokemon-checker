#!/usr/bin/env python3
import os
from database import create_database
from types_chart import create_types_chart
from create_trie import create_trie

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")
    database_path = os.path.join(data_dir, "database.csv")
    types_path = os.path.join(data_dir, "types_chart.csv")
    trie_path = os.path.join(data_dir, "pokemon_trie.json")
    limited = None

    if os.path.isfile(database_path) == False:
        print("Database not found. Please create database before venturing forth.")
        os.makedirs(data_dir, exist_ok=True)
    if os.path.isfile(types_path) == False:
        print("Types chart not found. Creating types chart")
        os.makedirs(data_dir, exist_ok=True)
        create_types_chart(types_path)
        return
    # Following is a limit to test function creating_database, it's not supposed to be used in regular use of a program.
    # limited = 10
    if limited == None:
        print("Creating database of all Pokémon.")
    else: 
        print(f"Creating database limited to {limited} number of entries.")
    create_database(database_path, limit=limited)
    create_trie(database_path, trie_path)
    print("Database created. Have fun.")
    return

main()