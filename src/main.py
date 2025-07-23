#!/usr/bin/env python3
import os
import shlex
from database import create_everything
from config import root_dir, data_dir, database_path, types_path, trie_path
from search import search_by_name, search_by_number, search_by_type
from fight import fight
from print_help import print_help
from pokemon_class import Pokemon
from present_results import display_search_results
from wrap_text import wrap_text

def parse_input(user_input):
    try:
        command = shlex.split(user_input)[0].lower()
        args = shlex.split(user_input)[1:]
        return command, args
    except ValueError as e:
        print(f"Error when handling input: {e}")
        return [], []

def main():
    limited = None
    force = False
    key_words = ["help", "exit", "quit", "q", "update", "search", "type", "fight"]

    print(wrap_text("Welcome to Pokémon Checker!"))
    print(wrap_text("Please wait as I check if database is present."))
    result = create_everything(force=force, limit=limited)
    if result == "cancel" and not os.path.isfile(database_path):
        print(wrap_text("Creation of database cancelled. Program can't work without database. Please run program again when you're ready to create database."))
        raise Exception("No database")
    print(wrap_text("Database detected. Have fun."))
    
    while True:
        print(wrap_text("Waiting for user input. Type \"help\" if you need instructions on usage:"))
        user_input = input(wrap_text(">>")).strip()
        

        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in key_words:
            if command == "help":
                print_help()
            elif command == "exit" or command == "quit" or command == "q":
                print(wrap_text("Goodbye :)"))
                break
            elif command == "update":
                create_everything(database_path, types_path, trie_path, data_dir, force=True, limit=limited)
            elif command == "search":
                if len(args) > 1:
                    print(wrap_text("Too many arguments used with command \"search\". If you're searching for a Pokémon with spaces in its name (like Tapu Koko), please use quotation marks."))
                    continue
                if len(args) == 0:
                    print(wrap_text("No search criteria detected. Please try again."))
                    continue
                if len(args) == 1:
                    if args[0].strip().isdigit():
                        pokemon = search_by_number(args[0])
                    else:
                        pokemon = search_by_name(args[0])
                    if isinstance(pokemon, Pokemon):
                        display_search_results(pokemon)
                    else:
                        print(wrap_text("Pokémon not found. Please check the name and try again."))
                        continue                    
            elif command == "type":
                if len(args) == 0:
                    print(wrap_text("No search criteria detected. Please try again."))
                    continue
                query = " ".join(args)
                search_by_type(query)
            elif command == "fight":
                if len(args) < 2:
                    print(wrap_text("Not enough arguments given. If you need reminder on usage type \"help\"."))
                    continue
                elif len(args) > 3:
                    print(wrap_text("Too many arguments used with command \"fight\". If you're searching for a Pokémon with spaces in its name (like Tapu Koko), please use quotation marks."))
                    continue
                elif len(args) == 2:
                    level = 50
                elif len(args) == 3:
                    level = args[2]
                pokemon1 = search_by_name(args[0])
                pokemon2 = search_by_name(args[1])
                if isinstance(pokemon1, Pokemon) and isinstance(pokemon2, Pokemon):
                    fight(pokemon1, pokemon2, level)
                else:
                    print(wrap_text("One or both of Pokémon not found. Please check the names and try again."))
                    continue
        else:
            print(wrap_text(f"Command: {command} not recognized. Please try again."))
            continue

main()