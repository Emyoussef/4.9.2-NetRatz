#!/bin/bash

# Remove existing Output.txt if it exists
rm Output.txt

# Provide input to the Python script and capture the output
echo "Running Python script with input..."
python3 test_Graphhopper.py << testFile > Output.txt
car  # Input
washinton,DC #Input
Baltimore,MD #Input
miles #input
q #input
testFile

