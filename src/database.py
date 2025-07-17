import requests
import time
import csv
#import os
from tqdm import tqdm
import json

def safe_request(url, max_retries=5, delay=5, fail_delay=60):
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response, delay
            else:
                attempt += 1
                print(f"Encountered HTTP error {response.status_code}, attempt {attempt}/{max_retries}. Retrying in {fail_delay}s...")
                if response.status_code == 429:
                    print(f"Error code 429 suggests too many requests. Increasing delay between attempts")
                    delay *= 2
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Connection error, attempt {attempt}/{max_retries}: {e}")

        if attempt == max_retries:
            print("Exceeded number of failed attempts for a single request. Terminating program.\nPlease check your internet connection or pokeapi.co status.")
            raise
        time.sleep(fail_delay)

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

def create_database(path_to_csv, limit=None):
    url = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'
    max_retries = 5
    delay = 0.2
    fail_delay = 60

    print("Starting process of creating Pokémon database.")
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
    
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    # data_dir = os.path.join(root_dir, "data")
    # csv_path = os.path.join(data_dir, "database.csv")
    csv_path = path_to_csv
    # special_names = {"ho-oh": "Ho-Oh",
    #                  "porygon-z": "Porygon-Z",
    #                  "jangmo-o": "Jangmo-O",
    #                  "hakamo-o": "Hakamo-o",
    #                  "kommo-o": "Kommo-o",
    #                  "ting-lu": "Ting-Lu",
    #                  "chien-pao": "Chien-Pao",
    #                  "wo-chien": "Wo-Chien",
    #                  "chi-yu": "Chi-Yu",
    #                  "mr-mime": "Mr. Mime",
    #                  "mime-jr": "Mime Jr.",
    #                  "mr-rime": "Mr. Rime",
    #                  "farfetchd": "Farfetch'd",
    #                  "sirfetchd": "Sirfetch'd",
    #                  "type-null": "Type: Null",
    #                  }
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)  
        writer.writerow(['National Dex', 'Name', 'Types', 'Abilities', 'Stats', 'Base Stats Total'])  
        for i in tqdm(range(0, number_of_pokemon), desc="Fetching Pokémon data..."):
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
            national_dex = int(data['species']['url'].split("/")[-2])
            name = data['name']
            # if name in special_names:
            #     name = special_names[name]
            # else:
            #     name = name.replace("-", " ").title().replace(" ", "-")
            name = proper_name(name)
            if "gmax" in name.lower():
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
    return

if __name__ == "__main__":
    print("This function is not supposed to be run directly.")
    print("Please use main.py to work with the database.")
    exit(1)