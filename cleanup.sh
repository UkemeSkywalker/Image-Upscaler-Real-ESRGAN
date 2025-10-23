#!/bin/bash

echo "Cleaning up Real-ESRGAN folder..."

# Create trash directory
mkdir -p trash

# Move unnecessary files/folders to trash
echo "Moving development and documentation files to trash..."

# Development/CI files
mv .github trash/ 2>/dev/null
mv .gitignore trash/ 2>/dev/null
mv .pre-commit-config.yaml trash/ 2>/dev/null

# Documentation and assets
mv assets trash/ 2>/dev/null
mv docs trash/ 2>/dev/null
mv README.md trash/ 2>/dev/null
mv README_CN.md trash/ 2>/dev/null

# Development/training files
mv experiments trash/ 2>/dev/null
mv options trash/ 2>/dev/null
mv scripts trash/ 2>/dev/null
mv tests trash/ 2>/dev/null

# Sample inputs (keep a few for testing)
mkdir -p trash/inputs
mv inputs/video trash/inputs/ 2>/dev/null
mv inputs/00003.png trash/inputs/ 2>/dev/null
mv inputs/00017_gray.png trash/inputs/ 2>/dev/null
mv inputs/0030.jpg trash/inputs/ 2>/dev/null
mv inputs/ADE_val_00000114.jpg trash/inputs/ 2>/dev/null
mv inputs/children-alpha.png trash/inputs/ 2>/dev/null
mv inputs/OST_009.png trash/inputs/ 2>/dev/null
mv inputs/tree_alpha_16bit.png trash/inputs/ 2>/dev/null
mv inputs/wolf_gray.jpg trash/inputs/ 2>/dev/null
# Keep 0014.jpg for testing

# Build artifacts
mv realesrgan.egg-info trash/ 2>/dev/null

# Other files
mv CODE_OF_CONDUCT.md trash/ 2>/dev/null
mv cog_predict.py trash/ 2>/dev/null
mv cog.yaml trash/ 2>/dev/null
mv inference_realesrgan_video.py trash/ 2>/dev/null
mv LICENSE trash/ 2>/dev/null
mv setup.cfg trash/ 2>/dev/null

echo "Cleanup complete!"
echo "Moved unnecessary files to trash/ folder"
echo ""
echo "Essential files remaining:"
echo "- realesrgan/ (package)"
echo "- inference_realesrgan.py (main script)"
echo "- server.py, upscaler.py (server files)"
echo "- requirements*.txt, setup.py (installation)"
echo "- weights/ (models)"
echo "- inputs/0014.jpg (test image)"