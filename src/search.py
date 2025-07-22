import csv
import os
import json
from create_trie import import_trie
from database import proper_name, create_type_list
from config import database_path, types_path, data_dir, trie_path
from pokemon_class import Pokemon

def search_by_number(query, attempts_so_far=0, max_attempts=5):
    with open(database_path, mode='r', newline='', encoding='utf-8') as file:
        data = list(csv.reader(file))[1:]
        attempt = attempts_so_far
        attempt_choice = attempts_so_far
        max_attempts = max_attempts
        while attempt < max_attempts:
            clean_query = query.strip()
            clean_query = clean_query.lstrip("0")
            
            if clean_query == "":
                print(f"Invalid input, there's no Pokémon with Pokédex number: {query}")
                attempt += 1
                if attempt == max_attempts:
                    print("Too many failed attempts. Terminating search.")
                    return None
                print("Please try again. You can type \"exit\" to return to main menu.")
                query = input("Waiting for Pokédex number input:\n>>")
                continue

            if not clean_query.isdigit():
                return search_by_name(clean_query, database_path, attempts_so_far=attempt, max_attempts=max_attempts)

            results = []

            for row in data:
                if row[0].lstrip("0") == clean_query:
                    number = row[0]
                    name = row[1]
                    types = row[2]
                    abilities = row[3]
                    stats = json.loads(row[4])
                    bst = row[5]
                    pokemon = [number, name, types, abilities, stats, bst]
                    results.append(pokemon)

            if len(results) == 0:
                attempt += 1
                print(f"Pokémon with specified Pokédex number({clean_query}) not found. Make sure to input proper Pokédex number.")
                if attempt == max_attempts:
                    print("Too many failed attempts. Terminating search.")
                    return None
                print("Please try again. You can type \"exit\" to return to main menu.")
                query = input("Waiting for Pokédex number input:\n>>")
            elif len(results) == 1:
                print(f"Found Pokémon with Pokédex number {clean_query}, it's {results[0][1]}.")
                return Pokemon(*results[0])
            else:
                choices = "\n".join(f"{i+1} {result[1]}" for i, result in enumerate(results))
                normalized_results = {result[1].lower(): result for result in results}
                print(f"Found more than 1 match for this Pokédex number({clean_query}). It has more forms than one.")
                print(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}")
                while attempt_choice < max_attempts:
                    search = input("Waiting for name or number input:\n>>")
                    search = search.strip()
                    if search.isdigit():
                        search = search.lstrip("0")
                        if search == "":
                            attempt_choice += 1
                            if attempt_choice == max_attempts:
                                print("Too many failed attempts. Terminating search.")
                                return None
                            print("Please try again. You can type \"exit\" to return to main menu.")
                            continue
                        index = int(search)
                        if index > 0 and index <= len(results):
                            return Pokemon(*results[index - 1])
                        else:
                            attempt_choice += 1
                            if attempt_choice == max_attempts:
                                print("Too many failed attempts. Terminating search.")
                                return None
                            print(f"Specified number is out of list's range. Please try again(attempt {attempt_choice} out of {max_attempts}). You can type \"exit\" to return to main menu. Here's the list once again:\n{choices}")
                    elif search.lower() == "exit":
                        confirm = input(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?")
                        if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                            return None
                    elif search.lower() in normalized_results:
                        selected = normalized_results[search.lower()]
                        return Pokemon[*selected]
                    else:
                        attempt_choice += 1
                        if attempt_choice == max_attempts:
                            print("Too many failed attempts. Terminating search.")
                            return None
                        print(f"Incorrect name. Please try again(attempt {attempt_choice} out of {max_attempts}). You can type \"exit\" to return to main menu. Here's the list once again:\n{choices}")

def search_by_name(query, attempts_so_far=0, max_attempts=5):
    pokemon_trie = import_trie(trie_path)
    
    attempt_choice = attempts_so_far
    attempt = attempts_so_far
    max_attempts = max_attempts

    while attempt < max_attempts:
        query = query.lower().strip()
        if query == "exit":
            confirm = input(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?\n>>")
            if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                return None
        results = list(pokemon_trie.iterkeys(prefix=query))
        if len(results) == 0:
            attempt += 1
            print(f"No Pokémon matching prefix: \"{query}\" found.")
            if attempt == max_attempts:
                print("Too many failed attempts. Terminating search.")
                return None
            else:
                print("Please try again. You can type \"exit\" to return to main menu.")
                query = input("Waiting for Pokémon name input:\n>>")
        elif len(results) == 1:
            print("Found Pokémon")
            return Pokemon(*pokemon_trie[results[0]])
        else:
            choices = "\n".join(f"{i+1} {result[1]}" for i, result in enumerate(results))
            normalized_results = {result[1].lower(): result for result in results}
            print(f"Found more than 1 match for this search term(\"{query}\").")
            print(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}")
            while attempt_choice < max_attempts:
                search = input("Waiting for name or number input:\n>>")
                search = search.strip()
                if search.isdigit():
                    search = search.lstrip("0")
                    index = int(search)
                    if index > 0 and index <= len(results):
                        return Pokemon(*pokemon_trie[results[index - 1]])
                    else:
                        attempt_choice += 1
                        if attempt_choice == max_attempts:
                            print("Too many failed attempts. Terminating search.")
                            return None
                        print(f"Specified number is out of list's range. Please try again(attempt {attempt_choice} out of {max_attempts}). Here's the list once again:\n{choices}")
                elif search.lower() == "exit":
                    confirm = input(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?\n>>")
                    if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                        return None
                elif search.lower() in normalized_results:
                    selected = normalized_results[search.lower()]
                    return Pokemon(*selected)
                else:
                    attempt_choice += 1
                    if attempt_choice == max_attempts:
                        print("Too many failed attempts. Terminating search.")
                        return None
                    print(f"Incorrect name. Please try again(attempt {attempt_choice} out of {max_attempts}). Here's the list once again:\n{choices}")

def search_by_type(query):
    attempt = 0
    max_attempts = 5
    list_of_types = create_type_list(types_path)

    while attempt < max_attempts:
        types_to_search = query.split()

        if types_to_search[0].lower() == "exit":
            confirm = input(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for type \"exit\"?\n>>")
            if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                return None

        if len(types_to_search) != 1 and len(types_to_search) != 2:
            attempt += 1
            if attempt == max_attempts:
                print("Too many failed attempts. Terminating search.")
                return None
            print("Incorrect usage of function. Try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu.")
            query = input("Waiting for type name(s) input:\n>>")
        else:
            if types_to_search[0].capitalize() not in list_of_types:
                attempt += 1
                if attempt == max_attempts:
                    print("Too many failed attempts. Terminating search.")
                    return None
                print(f"Type {types_to_search[0]} is wrong name of type. Please try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu.")
                query = input("Waiting for type name(s) input:\n>>")
            else:
                path_to_type_file = os.path.join(data_dir, f'{types_to_search[0]}.csv')
                with open(path_to_type_file, mode='r', newline='', encoding='utf-8') as type_file:
                    data = csv.reader(type_file)
                    list_of_pokemon = []
                    if len(types_to_search) == 2:
                        if types_to_search[1].capitalize() not in list_of_types:
                            attempt += 1
                            if attempt == max_attempts:
                                print("Too many failed attempts. Terminating search.")
                                return None
                            print(f"Type {types_to_search[1]} is wrong name of type. Please try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu.")
                            query = input("Waiting for type name(s) input:\n>>")
                            continue
                    for row in data:
                        if len(types_to_search) == 1:
                            list_of_pokemon.append((int(row[0]), row[1]))
                        elif row[2] == types_to_search[1].capitalize():
                            list_of_pokemon.append((int(row[0]), row[1]))
                    if len(list_of_pokemon) == 0:
                        print(f"No Pokémon found matching the search criteria.")
                        return None
                    sorted_list = sorted(list_of_pokemon, key=lambda x: x[0])
                    lines = []
                    for entry in sorted_list:
                        lines.append(f"{entry[0]}. {entry[1]}")
                    result = "\n".join(lines)

            print("Below is a list with Pokémon of specified types. Its format is <Pokédex number>. <Pokémon name>")
            print(result)
            print("If you want more detailed information about any Pokémon type: \"search <Pokémon name>\" or \"search <Pokédex number>\"")
            return