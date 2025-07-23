import requests
import time
import csv
import json
#import os
from tqdm import tqdm
from safe_request import safe_request
from config import types_path
from wrap_text import wrap_text

def create_types_chart():
    url = 'https://pokeapi.co/api/v2/type/?limit=100'
    # fail_count = 0
    max_retries = 5
    delay = 0.2
    fail_delay = 60

    print(wrap_text("Starting process of creating Pokémon type chart"))
    # number_of_types_check = requests.get(url)
    # while number_of_types_check.status_code != 200 and fail_count < max_retries:
    #     fail_count += 1
    #     if fail_count == max_retries:
    #         print("Encountered an error when requesting response from API.\nToo many failured attempts. Terminating program.")
    #         raise Exception(f"Failed to connect to API after {max_retries} attempts.")
    #     print(f"Encountered an error fetching data from API(attempt{fail_count}/{max_retries}).\nRetrying in one minute.")
    #     time.sleep(60)
    #     print("Retrying request...")
    #     number_of_types_check = requests.get(url)
    number_of_types_check, delay = safe_request(url, max_retries=max_retries, delay=delay, fail_delay=fail_delay)

    list_data = number_of_types_check.json()
    total_types = list_data['count']
    list_of_types = []
    for i in range(total_types - 2):
        list_of_types.append(list_data['results'][i]['name'].capitalize())
    base_dictionary = {}
    for type in list_of_types:
        base_dictionary[type] = 1

    with open(types_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)  
        writer.writerow(['Type', 'Dictionary of defensive type effectiveness', 'Dictionary of offensive type effectiveness'])
        for i in tqdm(range(0, total_types - 2), desc="Fetching Pokémon data..."): #Number of types is decreased by 2, because, as of creating this program, last two typeps are types not used in case of normal Pokémon(unknown and shadow), let's hope this won't change in the future
            data_url = list_data['results'][i]['url']

            # response = requests.get(data_url)
            # while response.status_code != 200 and fail_count < max_retries:
            #     fail_count += 1
            #     if fail_count == max_retries:
            #         print("Encountered an error when requesting response from API.\nToo many failured attempts. Terminating program.")
            #         raise Exception(f"Failed to connect to API after {max_retries} attempts.")
            #     print(f"Encountered an error fetching data from API(attempt{fail_count}/{max_retries}).\nRetrying in one minute.")
            #     time.sleep(60)
            #     if response.status_code == 429:
            #         print("Encountered 'Too Many Requests' error code, increasing delay for further requests.")
            #         delay *= 2
            #     print("Retrying request...")
            #     response = requests.get(data_url)
            response, delay = safe_request(data_url, max_retries=max_retries, delay=delay, fail_delay=fail_delay)

            data = response.json()
            type_name = data['name'].capitalize()

            defensive_dictionary = base_dictionary.copy()
            double_damage_from = []
            for entry in data['damage_relations']['double_damage_from']:
                double_damage_from.append(entry['name'])
            half_damage_from = []
            for entry in data['damage_relations']['half_damage_from']:
                half_damage_from.append(entry['name'])
            no_damage_from = []
            for entry in data['damage_relations']['no_damage_from']:
                no_damage_from.append(entry['name'])
                
            offensive_dictionary = base_dictionary.copy()
            double_damage_to = []
            for entry in data['damage_relations']['double_damage_to']:
                double_damage_to.append(entry['name'])
            half_damage_to = []
            for entry in data['damage_relations']['half_damage_to']:
                half_damage_to.append(entry['name'])
            no_damage_to = []
            for entry in data['damage_relations']['no_damage_to']:
                no_damage_to.append(entry['name'])
                
            for t in defensive_dictionary:
                if t.lower() in double_damage_from:
                    defensive_dictionary[t] = 2
                elif t.lower() in half_damage_from:
                    defensive_dictionary[t] = 0.5
                elif t.lower() in no_damage_from:
                    defensive_dictionary[t] = 0

            for t in offensive_dictionary:
                if t.lower() in double_damage_to:
                    offensive_dictionary[t] = 2
                elif t.lower() in half_damage_to:
                    offensive_dictionary[t] = 0.5
                elif t.lower() in no_damage_to:
                    offensive_dictionary[t] = 0
            writer.writerow([type_name, json.dumps(defensive_dictionary), json.dumps(offensive_dictionary)])
            time.sleep(delay)
    return

if __name__ == "__main__":
    print(wrap_text("This function is not supposed to be run directly."))
    print(wrap_text("Please use main.py to work with the database."))
    exit(1)