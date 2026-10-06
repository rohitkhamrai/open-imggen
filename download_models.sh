#!/bin/bash
set -e

# Task 2: Pipeline Scaffolding (Download Models)

if [ ! -d "ComfyUI" ]; then
    echo "Error: ComfyUI directory not found. Please run setup_ubuntu.sh first."
    exit 1
fi

echo "Downloading Juggernaut XL..."
wget -O ComfyUI/models/checkpoints/juggernaut_xl.safetensors "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"

echo "Downloading SDXL VAE..."
wget -O ComfyUI/models/vae/sdxl_vae.safetensors "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors"

echo "Downloading IP-Adapter Plus SDXL models..."
wget -O ComfyUI/models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors"

echo "Downloading CLIP Vision models..."
wget -O ComfyUI/models/clip_vision/clip_vision_g.safetensors "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors"

echo "Models downloaded successfully!"
