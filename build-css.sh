#!/bin/bash

# Build Tailwind CSS for development
echo "Building Tailwind CSS..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Build CSS
echo "Building CSS from static/input.css to static/output.css..."
npx tailwindcss -i ./static/input.css -o ./static/output.css --minify

echo "CSS build complete!" 