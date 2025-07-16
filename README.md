# Pokemon-checker
A program used to check information about Pokemon.

## Requirements
- Python3
- requests
- pygtrie
- tqdm

## Usage
Clone repository and run `pip install -r requirements.txt`. Project has built-in database of Pokemon up to 9th generation. You use the program with `main.py`. The program will then instruct you on further usage.

## Notes
- Program works offline, using included database.
- Using `--force_update` to update the database requires internet connection and will take circa 5 minutes (more if ther're are any issues with connection).