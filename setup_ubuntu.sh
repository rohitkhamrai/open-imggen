#!/bin/bash
set -e

# Task 1: Environment Setup for sm_52 on Ubuntu

echo "Cloning ComfyUI..."
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing PyTorch with CUDA 12.6 support for sm_52..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

echo "Installing ComfyUI requirements..."
pip install -r requirements.txt

echo "Installing ComfyUI-Manager..."
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..

echo "Setup complete! Remember to launch with: python main.py --lowvram --fp32-vae --listen 0.0.0.0 --port 8188"
