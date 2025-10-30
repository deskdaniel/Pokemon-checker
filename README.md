# Pokemon-checker
An app running in **REPL** mode used to check information about Pokémon.

## Motivation
I used to play Pokémon some years ago and recently I encountered interesting fan-made game, which included Pokémon of all generations up to 8th. Considering that earlier I played only 3rd generation Pokémon games, there were a lot of Pokémon I didn't know, which required me to constantly look for them on wiki to know what I'm dealind with.
This lightweight local app is able to present the most important information about Pokémon helping you plan your matchups.

## Requirements
- Python3
- The following packages (installed automatically by the launcher scripts):
    - requests
    - pygtrie
    - tqdm

## Quick Start
1. Clone the repository.
2. Run the program:
    - Windows: use `run_windows.bat`
    - Linux/MacOS/WSL: use `run_unix.sh`

These launchers will create and activate virtual enviroment, install dependencies and run the program. You need to have Python 3 installed.

## Usage
After running the app you may type `help` to view detailed description of all available commands. Below is concise rundown of them:
-  `update` - forces update of local database. The only command that requires internet connection. Doesn't accept any arguments.
-  `search X` - search for Pokémon in database. Accepts argument **(X)**, which is either Pokédex number or Pokémon name (searching by prefix allowed). If more than one match is found, you'll be asked to pick one of them to present full information.
-  `type X` - search for Pokémon of given type. Argument **X** is a name of type(s). If you present more than one type as argument app will look for Pokémon that have **ALL** those types, meaning that searching for more than 3 types at the same time will always result in empty list (this might change in the future if Nintento decides to add 3rd type to Pokémon).
-  `fight X1 X2 lvl` - simulate very simple fight between 2 Pokemon. Arguments **X1* and **X2** are either Pokémon names or Pokédex numbers (can mix them - X1 might be Pokémon name and X2 Pokédex number or vice versa). Argument **lvl** is an integer in range 1-100, this is optional argument that will determine level used for fight. In general it shouldn't influence outcome of the fight as both Pokémon will always be the same level.

## Notes
- App works **offline**, using the bundled database (up to 9th generation).
- Using the `update` command requires internet connection and may take around **5-10 minutes**.
