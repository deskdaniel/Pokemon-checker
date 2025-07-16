import requests
import time
import csv
import json
#import os
from tqdm import tqdm

def create_types_chart(path_to_csv):
    
    url = 'https://pokeapi.co/api/v2/type/?limit=100'
    fail_count = 0
    max_retries = 5
    delay = 0.2

    print("Starting process of creating Pokémon type chart")
    number_of_types_check = requests.get(url)
    while number_of_types_check.status_code != 200 and fail_count < max_retries:
        fail_count += 1
        if fail_count == max_retries:
            print("Encountered an error when requesting response from API.\nToo many failured attempts. Terminating program.")
            raise Exception(f"Failed to connect to API after {max_retries} attempts.")
        print(f"Encountered an error fetching data from API(attempt{fail_count}/{max_retries}).\nRetrying in one minute.")
        time.sleep(60)
        print("Retrying request...")
        number_of_types_check = requests.get(url)

    list_data = number_of_types_check.json()
    total_types = list_data['count']
    list_of_types = []
    for i in range(total_types - 2):
        list_of_types.append(list_data['results'][i]['name'].capitalize())
    base_dictionary = {}
    for type in list_of_types:
        base_dictionary[type] = 1
    csv_path = path_to_csv

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)  
        writer.writerow(['Type', 'Dictionary of defensive type effectiveness'])
        for i in tqdm(range(0, total_types - 2), desc="Fetching Pokémon data..."): #Number of types is decreased by 2, because, as of creating this program, last two typeps are types not used in case of normal Pokémon(unknown and shadow), let's hope this won't change in the future
            data_url = list_data['results'][i]['url']
            fail_count = 0

            response = requests.get(data_url)
            while response.status_code != 200 and fail_count < max_retries:
                fail_count += 1
                if fail_count == max_retries:
                    print("Encountered an error when requesting response from API.\nToo many failured attempts. Terminating program.")
                    raise Exception(f"Failed to connect to API after {max_retries} attempts.")
                print(f"Encountered an error fetching data from API(attempt{fail_count}/{max_retries}).\nRetrying in one minute.")
                time.sleep(60)
                if response.status_code == 429:
                    print("Encountered 'Too Many Requests' error code, increasing delay for further requests.")
                    delay *= 2
                print("Retrying request...")
                response = requests.get(data_url)

            data = response.json()
            type_name = data['name']
            dictionary = base_dictionary.copy()
            double_damage_from = []
            for entry in data['damage_relations']['double_damage_from']:
                double_damage_from.append(entry['name'])
            half_damage_from = []
            for entry in data['damage_relations']['half_damage_from']:
                half_damage_from.append(entry['name'])
            no_damage_from = []
            for entry in data['damage_relations']['no_damage_from']:
                no_damage_from.append(entry['name'])
                
            for t in dictionary:
                if t.lower() in double_damage_from:
                    dictionary[t] = 2
                elif t.lower() in half_damage_from:
                    dictionary[t] = 0.5
                elif t.lower() in no_damage_from:
                    dictionary[t] = 0
            writer.writerow([type_name, json.dumps(dictionary)])
            time.sleep(delay)
    return

if __name__ == "__main__":
    print("This function is not supposed to be run directly.")
    print("Please use main.py to work with the database.")
    exit(1)