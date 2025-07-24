@echo off
rem Check if the virtual environment exists, if not, create it
if not exist .venv (
    py -m venv .venv
)

rem Activate the virtual environment
call .venv\Scripts\activate

rem Install dependencies from requirements.txt
python -m pip install -r requirements.txt

rem Run your main Python program
python src\main.py

rem Deactivate the virtual environment
deactivate

rem Keep the console window open after the program finishes
pause