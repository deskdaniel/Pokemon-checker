# Pokemon-checker
A program used to check information about Pokémon.

## Requirements
- Python3
- The following packages (installed automatically by the launcher scripts):
    - requests
    - pygtrie
    - tqdm

## Usage
1. Clone the repository.
2. Run the program:
    - Windows: use `run_windows.bat`
    - Linux/MacOS/WSL: use `run_unix.sh`

These launchers will create and activate virtual enviroment, install dependencies and run the program. You need to have Python 3 installed.

Project has built-in database of Pokémon up to 9th generation. The program will guide you through further usage.

## Notes
- Program works **offline**, using the bundled database.
- Using the `update` command requires internet connection and may take around **5-10 minutes**.