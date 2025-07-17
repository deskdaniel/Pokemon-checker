import csv
from create_trie import import_trie
import os
from database import proper_name

def search_by_number(query, database_path):
    query = query.lstrip("0")
    if query == "":
        print("Invalid input, there's no Pokémon with Pokédex number: 0")
        return
    else:
        with open(database_path, mode='r', newline='', encoding='utf-8') as file:
            data = list(csv.reader(file))[1:]
            attempt = 0
            attemp_choice = 0
            max_attempts = 5
            while attempt < max_attempts:
                results = []
                for row in data:
                    if row[0].lstrip("0") == query:
                        results.append(row[1])
                if len(results) == 0:
                    attempt += 1
                    print(f"Pokémon with specified Pokédex number({query}) not found. Make sure to input proper Pokédex number.")
                    if attempt == max_attempts:
                        print("Too many failed attempts. Terminating search.")
                        return None
                    print("Please try again.")
                    query = input("Waiting for Pokédex number input:")
                elif len(results) == 1:
                    print(f"Found Pokémon with Pokédex number {query}, it's {results[0]}.")
                    return results[0]
                else:
                    choices = "\n".join(f"{i+1} {name}" for i, name in enumerate(results))
                    normalized_results = {name.lower(): name for name in results}
                    print(f"Found more than 1 match for this Pokédex number({query}). It has more forms than one.")
                    print(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}")
                    while attemp_choice < max_attempts:
                        search = input("Waiting for name or number input:")
                        if search.isdigit():
                            search = search.lstrip("0")
                            index = int(search)
                            if index > 0 and index <= len(results):
                                return proper_name(results[index - 1])
                            else:
                                attemp_choice += 1
                                if attemp_choice == max_attempts:
                                    print("Too many failed attempts. Terminating search.")
                                    return None
                                print(f"Specified number is out of list's range. Please try again(attempt {attemp_choice} out of {max_attempts}). Here's the list once again:\n{choices}")
                        elif search.lower() in normalized_results:
                            return normalized_results[search.lower()]
                        else:
                            attemp_choice += 1
                            if attemp_choice == max_attempts:
                                print("Too many failed attempts. Terminating search.")
                                return None
                            print(f"Incorrect name. Please try again(attempt {attemp_choice} out of {max_attempts}). Here's the list once again:\n{choices}")

def search_by_name(query, database_path):
    path_to_json = os.path.join(os.path.dirname(database_path), "pokemon_trie.json")
    pokemon_trie = import_trie(path_to_json)
    
    attemp_choice = 0
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        query = query.lower().strip(" ")
        results = list(pokemon_trie.iterkeys(prefix=query))
        if len(results) == 0:
            attempt += 1
            print(f"No Pokémon matching prefix: \"{query}\" found.")
            if attempt == max_attempts:
                print("Too many failed attempts. Terminating search.")
                return None
            else:
                print("Please try again.")
                query = input("Waiting for Pokémon name input:")
        elif len(results) == 1:
            print("Found Pokémon")
            return pokemon_trie[results[0]]
        else:
            choices = "\n".join(f"{i+1} {name}" for i, name in enumerate(results))
            normalized_results = {name.lower(): name for name in results}
            print(f"Found more than 1 match for this search term(\"{query}\").")
            print(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices}")
            while attemp_choice < max_attempts:
                search = input("Waiting for name or number input:")
                if search.isdigit():
                    search = search.lstrip("0")
                    index = int(search)
                    if index > 0 and index <= len(results):
                        return pokemon_trie[results[index - 1]]
                    else:
                        attemp_choice += 1
                        if attemp_choice == max_attempts:
                            print("Too many failed attempts. Terminating search.")
                            return None
                        print(f"Specified number is out of list's range. Please try again(attempt {attemp_choice} out of {max_attempts}). Here's the list once again:\n{choices}")
                elif search.lower() in normalized_results:
                    return normalized_results[search.lower()]
                else:
                    attemp_choice += 1
                    if attemp_choice == max_attempts:
                        print("Too many failed attempts. Terminating search.")
                        return None
                    print(f"Incorrect name. Please try again(attempt {attemp_choice} out of {max_attempts}). Here's the list once again:\n{choices}")