#!/bin/bash

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
        echo "Python is not installed. Please install Python to continue."
        exit 1
    fi
}

# Function to create a virtual environment
create_venv() {
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv || python -m venv .venv
    else
        echo "Virtual environment already exists."
    fi
}

# Function to activate the virtual environment and install dependencies
install_dependencies() {
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi

    echo "Installing dependencies..."
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping dependency installation."
    fi
}

# Function to run the Flask application
run_flask() {
    echo "Running Flask application..."
    export FLASK_APP=app/run.py
    export FLASK_ENV=development
    flask run
}

# Main script execution
check_python
create_venv
install_dependencies
run_flask