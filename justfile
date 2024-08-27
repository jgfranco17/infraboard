# Print list of available recipe (this)
default:
    @just --list

# Install dependencies
install:
    @echo "Installing project dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    @echo "All Python dependencies installed!"

# Start the dashboard server
run port:
    @echo "Starting service monitoring app!"
    streamlit run main.py --server.port {{ port }}

# Run pytest suite
pytest *ARGS:
    @echo "Running PyTest..."
    pytest {{ARGS}}

# Get code coverage report
coverage:
    coverage run --source=infraboard --omit="*/__init__.py,*/test_*.py" -m pytest
    coverage report
