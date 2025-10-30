# Pokemon-checker
An app running in REPL mode that lets you check information about Pokémon.

## Motivation
I used to play Pokémon years ago and recently came across an interesting fan-made game that included Pokémon from all generations up to the 8th.
Since I had only played 3rd-generation games before, there were many Pokémon I didn’t recognize — and I constantly had to check wikis to understand what I was dealing with.

This lightweight local app helps by displaying essential information about Pokémon, making it easier to plan matchups without needing to go online.

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
  
These launcher scripts will:
- Create and activate a virtual environment,
- Install dependencies,
- Run the program.

You only need to have Python 3 installed beforehand.

## Usage
After starting the app, type `help` to see a full list of available commands.
Below is a brief overview:
-  `update` - forces update of local database. This is the only command that requires internet access. Takes no arguments.
-  `search X` - searches for Pokémon in the database. Argument **(X)** can be either a Pokédex number or a Pokémon name (prefix search supported). If multiple matches are found, you’ll be asked to choose one for detailed info.
-  `type X` - list Pokémon by type. Argument **X** is the name of one or more types. If multiple types are given, only Pokémon that have **ALL** those types are shown. Searching for more than 2 types will return no results, as no Pokémon currently has more than 2 types.
-  `fight X1 X2 lvl` - simulates a simple battle between two Pokémon. **X1** and **X2** can be names or Pokédex numbers (mixing is allowed). Optional **lvl** sets the level for the fight (1–100). In general, level does not affect the outcome since both Pokémon will use the same level.

## Notes
- The app works offline, using the bundled Pokémon database (up to generation 9).
- The `update` command requires an internet connection and may take **5–10 minutes** to complete.
