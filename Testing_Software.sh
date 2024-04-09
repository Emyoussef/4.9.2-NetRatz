#!/bin/bash

run_tests() {
    echo "Running tests..."
    python3 -m pytest
}

echo "Checking out code..."
python3 Graphhopper_App.py

run_tests

if [ $? -eq 0 ]; then
    echo "All tests passed!"

else
    echo "Tests failed!"
    exit 1
fi
