# Print list of available recipe (this)
_default:
    @just --list --unsorted

# Install dependencies
install:
    #!/usr/bin/env bash
    echo "Installing project dependencies..."
    if ! command -v uv &> /dev/null
    then
        echo "Poetry has not been installed."
        echo "Please install with `pip install uv` to continue"
        exit 1
    fi
    uv sync
    echo "All Python dependencies installed!"

# Start the dashboard server
run port:
    @echo "Starting service monitoring app!"
    uv run streamlit run main.py --server.port {{ port }}

# Run pytest suite
pytest *args:
    @echo "Running PyTest..."
    @uv run pytest {{ args }}

# Get code coverage report
coverage:
    uv run coverage run --source=infraboard --omit="*/__init__.py,*/test_*.py" -m pytest
    uv run coverage report
