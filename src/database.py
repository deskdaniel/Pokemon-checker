import requests
import time
import csv
import os
import json
import ast
from tqdm import tqdm
from create_trie import create_trie
from types_chart import create_types_chart
from safe_request import safe_request
from wrap_text import wrap_text
from config import database_path, types_path, trie_path, data_dir

def proper_name(name):
    special_names = {"ho-oh": "Ho-Oh",
                    "ho oh": "Ho-Oh",
                    "porygon-z": "Porygon-Z",
                    "porygon z": "Porygon-Z",
                    "jangmo-o": "Jangmo-O",
                    "jangmo o": "Jangmo-O",
                    "hakamo-o": "Hakamo-o",
                    "hakamo o": "Hakamo-o",
                    "kommo-o": "Kommo-o",
                    "kommo o": "Kommo-o",
                    "ting-lu": "Ting-Lu",
                    "ting lu": "Ting-Lu",
                    "chien-pao": "Chien-Pao",
                    "chien pao": "Chien-Pao",
                    "wo-chien": "Wo-Chien",
                    "wo chien": "Wo-Chien",
                    "chi-yu": "Chi-Yu",
                    "chi yu": "Chi-Yu",
                    "mr-mime": "Mr. Mime",
                    "mr mime": "Mr. Mime",
                    "mr.mime": "Mr. Mime",
                    "mime-jr": "Mime Jr.",
                    "mime jr": "Mime Jr.",
                    "mr-rime": "Mr. Rime",
                    "mr rime": "Mr. Rime",
                    "mr.rime": "Mr. Rime",
                    "farfetchd": "Farfetch'd",
                    "farfetch d": "Farfetch'd",
                    "sirfetchd": "Sirfetch'd",
                    "sirfetch d": "Sirfetch'd",
                    "type-null": "Type: Null",
                    "type null": "Type: Null",
                    "type:null": "Type: Null",
                    }
    if name in special_names:
        proper_name = special_names[name]
    else:
        proper_name = name.replace("-", " ").title()
    return proper_name

def create_database(limit=None):
    url = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'
    max_retries = 5
    delay = 0.2
    fail_delay = 60

    print(wrap_text("Starting process of creating Pokémon database."))
    # number_check = requests.get(url)
    # while number_check.status_code != 200 and fail_count < max_retries:
    #     fail_count += 1
    #     if fail_count == max_retries:
    #         print("Encountered an error when requesting response from API.\nToo many failed attempts. Terminating program.")
    #         raise Exception(f"Failed to connect to API after {max_retries} attempts.")
    #     print(f"Encountered an error fetching data from API(attempt{fail_count}/{max_retries}).\nRetrying in one minute.")
    #     time.sleep(60)
    #     print("Retrying request...")
    #     number_check = requests.get(url)
    number_check, delay = safe_request(url, max_retries=max_retries, delay=delay, fail_delay=fail_delay)
    
    list_data = number_check.json()
    total_pokemon = list_data['count']
    if limit != None:
        number_of_pokemon = min(total_pokemon, limit)
    else:
        number_of_pokemon = total_pokemon

    if limit == None:
        print(wrap_text(f"Creating database, consisting of {number_of_pokemon} Pokémon."))
    else:
        print(wrap_text(f"Creating database consiting of {limit} Pokémon."))
    with open(database_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        writer.writerow(['Expected Pokémon Count:', total_pokemon])  
        writer.writerow(['National Dex', 'Name', 'Types', 'Abilities', 'Stats', 'Base Stats Total'])
        reduce_count = 0  
        for i in tqdm(range(0, number_of_pokemon), desc="Fetching Pokémon data..."):
            data_url = list_data['results'][i]['url']

            response, delay = safe_request(data_url, max_retries=max_retries, delay=delay, fail_delay=fail_delay)
            
            data = response.json()
            national_dex = int(data['species']['url'].split("/")[-2])
            name = data['name']
            name = proper_name(name)
            if "gmax" in name.lower():
                reduce_count += 1
                time.sleep(delay)
                continue
            types_sorted = sorted(data['types'], key=lambda x: x['slot'])
            types_names = []
            for t in types_sorted:
                types_names.append(t['type']['name'].capitalize())
            abilities_sorted = sorted(data['abilities'], key=lambda x: x['slot'])
            abilities_names = []
            for a in abilities_sorted:
                abilities_names.append(a['ability']['name'].replace("-", " ").title())
            stats = {}
            base_stats_total = 0
            for stat in data['stats']:
                stat_name = stat['stat']['name']
                if stat_name == "hp":
                    stat_name = stat_name.upper()
                else:
                    stat_name = stat_name.capitalize()
                value = stat['base_stat']
                stats[stat_name] = value
                base_stats_total += value
            writer.writerow([national_dex, name, str(types_names), str(abilities_names), json.dumps(stats), base_stats_total])
            time.sleep(delay)
    if reduce_count > 0:
        with open(database_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = list(csv.reader(csv_file))
            new_count = total_pokemon - reduce_count

        reader[0] = ['Expected Pokémon Count:', new_count]

        with open(database_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            writer.writerows(reader)

    return

if __name__ == "__main__":
    print(wrap_text("This function is not supposed to be run directly."))
    print(wrap_text("Please use main.py to work with the database."))
    exit(1)

def create_type_pokemon_list(wanted_type):
    list_of_types = create_type_list()
    
    if wanted_type not in list_of_types:
        raise Exception(f"Type \"{wanted_type}\" doesn't seem to exist. Make sure type name is correct.")
    
    print(wrap_text(f"Creating file: list of Pokémon with {wanted_type} type"))
    type_file_path = os.path.join(os.path.dirname(database_path), f'{wanted_type}.csv')
    
    with open(database_path, mode='r', newline='', encoding='utf-8') as file:
        data = csv.reader(file)
        next(data)
        next(data)
        with open(type_file_path, mode='w', newline='', encoding='utf-8') as type_file:
            writer = csv.writer(type_file, quoting=csv.QUOTE_ALL)
            writer.writerow(['Pokédex number','Pokémon name', 'Second type'])
            written = 0
            for row in data:
                types_list = ast.literal_eval(row[2])
                if wanted_type in types_list:
                    pokemon_name = row[1]
                    pokemon_number = row[0]
                    if len(types_list) > 1:
                        if types_list[0] == wanted_type:
                            second_type = types_list[1]
                        else:
                            second_type = types_list[0]
                    else:
                        second_type = "None"
                    writer.writerow([pokemon_number, pokemon_name, second_type])
                    written += 1
                    
    if written == 0:
        print(wrap_text(f"No Pokémon with {wanted_type} found. Deleting file {wanted_type}.csv"))
        os.remove(type_file_path)
    
def create_everything(force=False, limit=None):
    if not os.path.isdir(data_dir):
        print(wrap_text("Data directory not found, creating it together with its contents."))
        os.makedirs(data_dir, exist_ok=True)
        force = True
    elif not os.path.isfile(database_path):
        print(wrap_text("File database.csv not found. Creating all files."))
        force = True

    if os.path.isfile(database_path):
        with open(database_path, mode='r', newline='', encoding='utf-8') as csv_file:
            data = list(csv.reader(csv_file))
            count = data[0][1]
            try:
                if int(count) + 2 != len(data):
                    print(wrap_text("File database.csv found, but its length is not correct. Creating all files."))
                    force = True
                else:
                    print(wrap_text("File database.csv found and its length is as expected."))
            except (IndexError, ValueError):
                print(wrap_text("File database.csv found, but it's not complete. Creating all files."))
                force = True

    
    if force:
        print(wrap_text("You're about to update entire database. It should take approximately 5-10 minutes. Do you want to continue [Y(es)]?"))
        confirm = input(">>")
        confirm = confirm.strip()
        if confirm.lower() == "y" or confirm.lower() == "yes":
            print(wrap_text("Recreating database. Please wait."))
            create_database(limit=limit)
            create_trie()
            create_types_chart()
            create_type_files()
            return
        else:
            print(wrap_text("Recreating of database cancelled."))
            return "cancel"
    
    if not os.path.isfile(trie_path):
        print(wrap_text("Trie not found. Creating it."))
        create_trie()

    if not os.path.isfile(types_path):
        print(wrap_text("File types_chart.csv not found. Creating it."))
        create_types_chart()
        create_type_files()
        return
    
    list_of_types = create_type_list()
    for wanted_type in list_of_types:
        if not os.path.isfile(os.path.join(data_dir, f'{wanted_type}.csv')):
            create_type_pokemon_list(wanted_type)


def create_type_files():
    list_of_types = create_type_list()
    for wanted_type in list_of_types:
        create_type_pokemon_list(wanted_type)

def create_type_list():
    with open(types_path, mode='r', newline='', encoding='utf-8') as file:
        data = csv.reader(file)
        next(data)
        list_of_types = []
        for row in data:
            list_of_types.append(row[0])
    return list_of_types