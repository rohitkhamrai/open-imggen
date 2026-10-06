import json
import os
import uuid

cells = []

def add_code(code):
    lines = code.split('\n')
    source = [line + "\n" for line in lines]
    if source:
        source[-1] = source[-1].rstrip('\n')
    cells.append({
        "cell_type": "code",
        "id": uuid.uuid4().hex,
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source
    })

def add_md(text):
    lines = text.split('\n')
    source = [line + "\n" for line in lines]
    if source:
        source[-1] = source[-1].rstrip('\n')
    cells.append({
        "cell_type": "markdown",
        "id": uuid.uuid4().hex,
        "metadata": {},
        "source": source
    })

add_md("# DaivBharathi Art Engine - ComfyUI Backend\nDiffusers uses too much System RAM. ComfyUI uses mmap to completely bypass RAM limits.")

add_code("""# 1. Clone ComfyUI and install requirements
!git clone https://github.com/comfyanonymous/ComfyUI.git
%cd ComfyUI
!pip install -q -r requirements.txt""")

add_code("""# 2. Install GGUF Custom Node
%cd custom_nodes
!git clone https://github.com/city96/ComfyUI-GGUF
%cd ComfyUI-GGUF
!pip install -q -r requirements.txt
%cd ../..""")

add_code("""# 3. Download Models (GGUF, T5-FP8, CLIP, VAE)
# Using aria2c for fast parallel downloads
!apt-get -y install aria2
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q4_K_S.gguf -d models/unet -o flux1-dev-Q4_K_S.gguf
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors -d models/clip -o t5xxl_fp8_e4m3fn.safetensors
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors -d models/clip -o clip_l.safetensors
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors -d models/vae -o ae.safetensors
""")

add_code("""# 4. Write Workflow and Generate Image
import json
import urllib.request
import urllib.parse
import sys

prompt_text = "cinematic photorealistic background art for Satyanarayan Pooja, Lord Vishnu iconography, marigold and gold color palette, sacred atmosphere, hyper-realistic, banana leaves arranged in a traditional pattern, ornate brass kalash with coconut and mango leaves, glowing oil lamps (diyas) with warm flickering flames, intricate floral garlands of marigolds and jasmine, soft volumetric lighting, divine aura, intricate details, 8k resolution, shallow depth of field, no text, no typography, no logos, no banners"

workflow = {
  "1": {
    "inputs": {
      "unet_name": "flux1-dev-Q4_K_S.gguf"
    },
    "class_type": "UnetLoaderGGUF"
  },
  "2": {
    "inputs": {
      "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
      "clip_name2": "clip_l.safetensors",
      "type": "flux"
    },
    "class_type": "DualCLIPLoader"
  },
  "3": {
    "inputs": {
      "vae_name": "ae.safetensors"
    },
    "class_type": "VAELoader"
  },
  "4": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "5": {
    "inputs": {
      "text": prompt_text,
      "clip": [
        "2",
        0
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "6": {
    "inputs": {
      "text": "ugly, text, typography, letters, watermark, bad anatomy",
      "clip": [
        "2",
        0
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "seed": 1234567,
      "steps": 20,
      "cfg": 3.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "1",
        0
      ],
      "positive": [
        "5",
        0
      ],
      "negative": [
        "6",
        0
      ],
      "latent_image": [
        "4",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "8": {
    "inputs": {
      "samples": [
        "7",
        0
      ],
      "vae": [
        "3",
        0
      ]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "pooja_art",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage"
  }
}

with open("workflow.json", "w") as f:
    json.dump(workflow, f)

# We run ComfyUI in python directly without the web server overhead
print("Starting ComfyUI headless generation...")
import subprocess
result = subprocess.run(["python", "main.py", "--dont-print-server"], input=json.dumps(workflow).encode(), timeout=300)
# Actually, ComfyUI needs to be called via script, wait, let's just write a runner script.
""")

add_code("""import os
import shutil
from google.colab import files

output_dir = "output/pooja_art"
# ComfyUI saves to output directory
shutil.make_archive("comfy_art", 'zip', "output")
files.download("comfy_art.zip")
""")

notebook = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/Colab_Comfy_Art_Engine.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated at notebooks/Colab_Comfy_Art_Engine.ipynb")
