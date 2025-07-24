#!/bin/bash

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# echo "Installing dependencies..."
# if [ -f "$VENV_DIR/bin/pip" ]; then
#     "$VENV_DIR/bin/pip" install -r requirements.txt
# else
#     "$VENV_DIR/bin/pip3" install -r requirements.txt
# fi

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "Running the program..."
python src/main.py

echo "Deactivating virtual environment."
deactivate

echo "Program finished."