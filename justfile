# STF - Justfile utility

# Print list of available recipe (this)
default:
    @just --list

install:
    @echo "Installing project dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    @echo "All Python dependencies installed!"

run port:
    @echo "Starting service monitoring app!"
    streamlit run main.py --server.port {{ port }}

pytest *ARGS:
    @echo "Running PyTest..."
    pytest {{ARGS}}

coverage:
    coverage run --source=infraboard --omit="*/__init__.py,*/test_*.py" -m pytest
    coverage report
