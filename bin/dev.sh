#!/bin/bash
# dev.sh: Consolidated helper commands for the project.
# Usage: ./bin/dev.sh <command>
# Available commands: help, run_project, debug_project, clean_project, containerize_project, install_requirements, update_requirements, lint_project, run_tests, run_notebook, env_status

help() {
  cat <<HELP
Available commands:
  help                - Show this help message.
  run_project         - Activate the virtual environment and run src/main.py.
  debug_project       - Run src/main.py in debug mode using pdb.
  clean_project       - Clean up logs and temporary files.
  containerize_project- Build a Docker image for the project.
  install_requirements- Activate the virtual environment and install dependencies from requirements.txt.
  update_requirements - Update requirements.txt with currently installed packages (pip freeze).
  lint_project        - Run flake8 on the src/ directory.
  run_tests           - Run tests using pytest.
  run_notebook        - Start a Jupyter Lab server.
  env_status          - Display the current virtual environment details.
HELP
}

run_project() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  echo "Virtual environment activated."
  if [ -f "src/main.py" ]; then
    python src/main.py
  else
    echo "src/main.py not found."
  fi
  deactivate
}

debug_project() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  python -m pdb src/main.py
  deactivate
}

clean_project() {
  echo "Cleaning logs..."
  rm -rf logs/*
}

containerize_project() {
  echo "Building Docker image..."
  docker build -t ${PROJECT_NAME:-project} .
  echo "Docker build complete. (Enhance with docker-compose as needed)"
}

install_requirements() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
  else
    echo "No requirements.txt found. Skipping installation."
  fi
  deactivate
}

update_requirements() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  echo "Updating requirements.txt with installed packages..."
  pip freeze > requirements.txt
  echo "requirements.txt updated."
  deactivate
}

lint_project() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  echo "Running flake8 on src/..."
  flake8 src/
  deactivate
}

run_tests() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  echo "Running tests using pytest..."
  pytest
  deactivate
}

run_notebook() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Please run the setup script."
    exit 1
  fi
  source .venv/bin/activate
  echo "Starting Jupyter Lab..."
  jupyter lab
  # Alternatively, use: jupyter notebook
  # Note: This command will block until you stop the server.
}

env_status() {
  if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found."
    exit 1
  fi
  source .venv/bin/activate
  echo $VIRTUAL_ENV
  echo "Python Path":
  python -c "import sys; print(sys.executable)"
  echo "Python version:"
  python --version
  echo "Installed packages:"
  pip list
  deactivate
}

case "$1" in
  help)
    help
    ;;
  run_project)
    run_project
    ;;
  debug_project)
    debug_project
    ;;
  clean_project)
    clean_project
    ;;
  containerize_project)
    containerize_project
    ;;
  install_requirements)
    install_requirements
    ;;
  update_requirements)
    update_requirements
    ;;
  lint_project)
    lint_project
    ;;
  run_tests)
    run_tests
    ;;
  run_notebook)
    run_notebook
    ;;
  env_status)
    env_status
    ;;
  *)
    echo "Unknown command. Use './bin/dev.sh help' for available commands."
    exit 1
    ;;
esac
