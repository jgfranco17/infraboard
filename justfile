# Print list of available recipe (this)
default:
    @just --list

# Install dependencies
install:
    #!/usr/bin/env bash
    echo "Installing project dependencies..."
    if ! command -v poetry &> /dev/null
    then
        echo "Poetry has not been installed."
        echo "Please install with `pip install poetry` to continue"
        exit 1
    fi
    poetry install
    poetry shell
    echo "All Python dependencies installed!"

# Start the dashboard server
run port:
    @echo "Starting service monitoring app!"
    poetry run streamlit run main.py --server.port {{ port }}

# Run pytest suite
pytest *ARGS:
    @echo "Running PyTest..."
    poetry run pytest {{ARGS}}

# Get code coverage report
coverage:
    poetry run coverage run --source=infraboard --omit="*/__init__.py,*/test_*.py" -m pytest
    poetry run coverage report
