#!/bin/bash

echo "Setting up Real-ESRGAN Image Upscaler Server..."

# Install Real-ESRGAN dependencies first
echo "Installing Real-ESRGAN dependencies..."
pip install -r requirements.txt

# Install Real-ESRGAN package
echo "Installing Real-ESRGAN package..."
pip install --user -e .

# Install server dependencies
echo "Installing server dependencies..."
pip install -r requirements_server.txt

# Create weights directory
mkdir -p weights

# Download models
echo "Downloading models..."

# General model
if [ ! -f "weights/RealESRGAN_x4plus.pth" ]; then
    echo "Downloading general model..."
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights
fi

# Anime model
if [ ! -f "weights/RealESRGAN_x4plus_anime_6B.pth" ]; then
    echo "Downloading anime model..."
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P weights
fi

echo "Setup complete!"
echo "To start the server, run: python server.py"
echo "Server will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"