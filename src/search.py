import csv
import os
import json
import ast
from create_trie import import_trie
from database import proper_name, create_type_list
from config import database_path, types_path, data_dir, trie_path
from pokemon_class import Pokemon
from wrap_text import wrap_text

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
                print(wrap_text(f"Invalid input, there's no Pokémon with Pokédex number: {query}"))
                attempt += 1
                if attempt == max_attempts:
                    print(wrap_text("Too many failed attempts. Terminating search."))
                    return None
                print(wrap_text("Please try again. You can type \"exit\" to return to main menu."))
                print(wrap_text("Waiting for Pokédex number input:"))
                query = input(">>")
                continue

            if not clean_query.isdigit():
                return search_by_name(clean_query, attempts_so_far=attempt, max_attempts=max_attempts)

            results = []

            for row in data:
                if row[0].lstrip("0") == clean_query:
                    number = row[0]
                    name = row[1]
                    types = ast.literal_eval(row[2])
                    abilities = ast.literal_eval(row[3])
                    stats = json.loads(row[4])
                    bst = row[5]
                    pokemon = [number, name, types, abilities, stats, bst]
                    results.append(pokemon)

            if len(results) == 0:
                attempt += 1
                print(wrap_text(f"Pokémon with specified Pokédex number({clean_query}) not found. Make sure to input proper Pokédex number."))
                if attempt == max_attempts:
                    print(wrap_text("Too many failed attempts. Terminating search."))
                    return None
                print(wrap_text("Please try again. You can type \"exit\" to return to main menu."))
                print(wrap_text("Waiting for Pokédex number or Pokémon name input:"))
                query = input(">>")
            elif len(results) == 1:
                print(wrap_text(f"Found Pokémon with Pokédex number {clean_query}, it's {results[0][1]}."))
                return Pokemon(*results[0])
            else:
                choices = "\n".join(f"{i+1} {result[1]}" for i, result in enumerate(results))
                normalized_results = {result[1].lower(): result for result in results}
                print(wrap_text(f"Found more than 1 match for this Pokédex number({clean_query}). It has more forms than one."))
                print(wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}"))
                while attempt_choice < max_attempts:
                    print(wrap_text("Waiting for name or number input:"))
                    search = input(">>")
                    search = search.strip()
                    if search.isdigit():
                        search = search.lstrip("0")
                        if search == "":
                            attempt_choice += 1
                            if attempt_choice == max_attempts:
                                print(wrap_text("Too many failed attempts. Terminating search."))
                                return None
                            print(wrap_text("Please try again. You can type \"exit\" to return to main menu."))
                            continue
                        index = int(search)
                        if index > 0 and index <= len(results):
                            return Pokemon(*results[index - 1])
                        else:
                            attempt_choice += 1
                            if attempt_choice == max_attempts:
                                print(wrap_text("Too many failed attempts. Terminating search."))
                                return None
                            print(wrap_text(f"Specified number is out of list's range. Please try again(attempt {attempt_choice} out of {max_attempts}). You can type \"exit\" to return to main menu. Here's the list once again:\n{choices}"))
                    elif search.lower() == "exit":
                        print(wrap_text(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?"))
                        confirm = input(">>")
                        if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                            return None
                        print(wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}"))
                    elif search.lower() in normalized_results:
                        selected = normalized_results[search.lower()]
                        return Pokemon(*selected)
                    else:
                        attempt_choice += 1
                        if attempt_choice == max_attempts:
                            print(wrap_text("Too many failed attempts. Terminating search."))
                            return None
                        print(wrap_text(f"Incorrect name. Please try again(attempt {attempt_choice} out of {max_attempts}). You can type \"exit\" to return to main menu. Here's the list once again:\n{choices}"))

def search_by_name(query, attempts_so_far=0, max_attempts=5):
    pokemon_trie = import_trie()
    
    attempt_choice = attempts_so_far
    attempt = attempts_so_far
    max_attempts = max_attempts

    while attempt < max_attempts:
        query = query.lower().strip()
        if query.isdigit():
            return search_by_number(query, attempt, max_attempts)
        if query == "exit":
            print(wrap_text(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?"))
            confirm = input(">>")
            if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                return None
        try:
            results = list(pokemon_trie.iterkeys(prefix=query))
        except KeyError:
            attempt += 1
            print(wrap_text(f"No Pokémon matching prefix: \"{query}\" found."))
            if attempt == max_attempts:
                print(wrap_text("Too many failed attempts. Terminating search."))
                return None
            else:
                print(wrap_text("Please try again. You can type \"exit\" to return to main menu."))
                print(wrap_text("Waiting for Pokémon name or Pokédex number input:"))
                query = input(">>")
                continue
        
        if len(results) == 0:
            attempt += 1
            print(wrap_text(f"No Pokémon matching prefix: \"{query}\" found."))
            if attempt == max_attempts:
                print(wrap_text("Too many failed attempts. Terminating search."))
                return None
            else:
                print(wrap_text("Please try again. You can type \"exit\" to return to main menu."))
                print(wrap_text("Waiting for Pokémon name input:"))
                query = input(">>")
        elif len(results) == 1:
            print(wrap_text("Found Pokémon"))
            return Pokemon(*pokemon_trie[results[0]])
        else:
            choices = "\n".join(f"{i+1} {proper_name(result)}" for i, result in enumerate(results))
            normalized_results = [result.lower() for result in results]
            print(wrap_text(f"Found more than 1 match for this search term(\"{query}\")."))
            print(wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}"))
            while attempt_choice < max_attempts:
                print(wrap_text("Waiting for name or number input:"))
                search = input(">>")
                search = search.strip()
                if search.isdigit():
                    search = search.lstrip("0")
                    index = int(search)
                    if index > 0 and index <= len(results):
                        return Pokemon(*pokemon_trie[results[index - 1]])
                    else:
                        attempt_choice += 1
                        if attempt_choice == max_attempts:
                            print(wrap_text("Too many failed attempts. Terminating search."))
                            return None
                        print(wrap_text(f"Specified number is out of list's range. Please try again(attempt {attempt_choice} out of {max_attempts}). Here's the list once again:\n{choices}"))
                elif search.lower() == "exit":
                    print(wrap_text(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?"))
                    confirm = input(">>")
                    if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                        return None
                elif search.lower() in normalized_results:
                    # selected = normalized_results[search.lower()]
                    return Pokemon(*pokemon_trie[search.lower()])
                    # return Pokemon(*selected)
                else:
                    attempt_choice += 1
                    if attempt_choice == max_attempts:
                        print(wrap_text("Too many failed attempts. Terminating search."))
                        return None
                    print(wrap_text(f"Incorrect name. Please try again(attempt {attempt_choice} out of {max_attempts}). Here's the list once again:\n{choices}"))

def search_by_type(query):
    attempt = 0
    max_attempts = 5
    list_of_types = create_type_list()

    while attempt < max_attempts:
        types_to_search = query.split()

        if types_to_search[0].lower() == "exit":

            print(wrap_text(f"Input \"exit\" detected. Do you want to exit [Y(es)] or search for prefix \"exit\"?"))
            confirm = input(">>")
            if confirm.lower().strip() == "y" or confirm.lower().strip() == "yes":
                return None

        if len(types_to_search) != 1 and len(types_to_search) != 2:
            attempt += 1
            if attempt == max_attempts:
                print(wrap_text("Too many failed attempts. Terminating search."))
                return None
            print(wrap_text("Incorrect usage of function. Try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu."))
            print(wrap_text("Waiting for type name(s) input:"))
            query = input(">>")
        else:
            if types_to_search[0].capitalize() not in list_of_types:
                attempt += 1
                if attempt == max_attempts:
                    print(wrap_text("Too many failed attempts. Terminating search."))
                    return None
                print(wrap_text(f"Type {types_to_search[0]} is wrong name of type. Please try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu."))
                print(wrap_text("Waiting for type name(s) input:"))
                query = input(">>")
            else:
                type_to_search = types_to_search[0].capitalize()
                path_to_type_file = os.path.join(data_dir, f'{type_to_search}.csv')
                with open(path_to_type_file, mode='r', newline='', encoding='utf-8') as type_file:
                    data = csv.reader(type_file)
                    next(data)
                    list_of_pokemon = []
                    if len(types_to_search) == 2:
                        if types_to_search[1].capitalize() not in list_of_types:
                            attempt += 1
                            if attempt == max_attempts:
                                print(wrap_text("Too many failed attempts. Terminating search."))
                                return None
                            print(wrap_text(f"Type {types_to_search[1]} is wrong name of type. Please try again, but without typing \"type\" at the beginning. You can type \"exit\" to return to main menu."))
                            print(wrap_text("Waiting for type name(s) input:"))
                            query = input(">>")
                            continue
                    for row in data:
                        if len(types_to_search) == 1:
                            list_of_pokemon.append((int(row[0]), row[1]))
                        elif row[2] == types_to_search[1].capitalize():
                            list_of_pokemon.append((int(row[0]), row[1]))
                    if len(list_of_pokemon) == 0:
                        print(wrap_text(f"No Pokémon found matching the search criteria."))
                        return None
                    sorted_list = sorted(list_of_pokemon, key=lambda x: x[0])
                    lines = []
                    for entry in sorted_list:
                        lines.append(f"{entry[0]}. {entry[1]}")
                    result = "\n".join(lines)

                print(wrap_text("Below is a list with Pokémon of specified types. Its format is <Pokédex number>. <Pokémon name>"))
                print(result)
                print(wrap_text("If you want more detailed information about any Pokémon type: \"search <Pokémon name>\" or \"search <Pokédex number>\""))
                return