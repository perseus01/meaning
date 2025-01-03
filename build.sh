#!/bin/bash

SCRIPT_NAME="meaning.py"
OUTPUT_DIR="output"
TARGET_DIR=$(pwd)


if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: $SCRIPT_NAME not found!"
    exit 1
fi

echo "Creating python3 virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip3 install -r requirements.txt


echo "Compiling $SCRIPT_NAME..."
nuitka --onefile --output-dir=$OUTPUT_DIR $SCRIPT_NAME


if [ $? -ne 0 ]; then
    echo "Error: Failed to compile $SCRIPT_NAME!"
    exit 1
fi


BINARY_NAME=$(basename "$SCRIPT_NAME" .py)
BINARY_FILE="$OUTPUT_DIR/$BINARY_NAME.bin"

if [ ! -f "$BINARY_FILE" ]; then
    echo "Error: Binary file not found!"
    exit 1
fi

mv "$BINARY_FILE" "$TARGET_DIR/$BINARY_NAME"
chmod u+x $BINARY_FILE

echo "Cleaning up..."
rm -rf $OUTPUT_DIR
rm -rf .venv/

echo "Compilation complete. The binary has been placed in $TARGET_DIR/$BINARY_NAME."
