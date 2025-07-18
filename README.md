# Pokemon-checker
A program used to check information about Pokemon.

## Requirements
- Python3
- requests
- pygtrie
- tqdm

## Usage
1. Clone the repository.
2. Create a virtual environment (optional, but recommended): `python3 -m venv venv`
3. Activate venv:
Windows: powershell: `.\venv\Scripts\Activate.ps1`, cmd: `.\venv\Scripts\activate.bat`
Linux/macOS: `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Run program with symbolic link `main` in root of the project.
Project has built-in database of Pokemon up to 9th generation. The program will then instruct you on further usage.

## Notes
- Program works offline, using included database.
- Using `--force_update` to update the database requires internet connection and will take circa 5-10 minutes (more if ther're are any issues with connection).