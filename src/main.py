#!/usr/bin/env python3
import os
from database import create_everything# , create_database
# from types_chart import create_types_chart
# from create_trie import create_trie
from config import root_dir, data_dir, database_path, types_path, trie_path

def main():
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    # data_dir = os.path.join(root_dir, "data")
    # database_path = os.path.join(data_dir, "database.csv")
    # types_path = os.path.join(data_dir, "types_chart.csv")
    # trie_path = os.path.join(data_dir, "pokemon_trie.json")
    limited = None
    force = False
    
    # Redundant part of code, now function create_everything() takes care of checking if files exist
    # if os.path.isfile(database_path) == False:
    #     print("Database not found. Please create database before venturing forth.")
    #     os.makedirs(data_dir, exist_ok=True)
    # if os.path.isfile(types_path) == False:
    #     print("Types chart not found. Creating types chart")
    #     os.makedirs(data_dir, exist_ok=True)
    #     create_types_chart(types_path)
    #     return

    # Following is a limit to test function creating_database, it's not supposed to be used in regular use of a program.
    # limited = 10
    create_everything(database_path, types_path, trie_path, data_dir, force=force, limit=limited)
    print("Database created. Have fun.")
    return

main()