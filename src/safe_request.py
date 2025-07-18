import time
import requests

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