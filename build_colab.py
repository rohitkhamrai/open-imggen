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

add_md("# DaivBharathi Colab Art Engine (Phase 2)\nEnsure you connect to a **T4 GPU** instance (Runtime -> Change runtime type).")

add_code("""!pip install -q diffusers transformers accelerate sentencepiece protobuf gguf huggingface_hub optimum""")

add_md("### HuggingFace Login\nFLUX.1-dev is a gated model. You must accept the terms on HF and provide your token below.")

add_code("""from huggingface_hub import notebook_login
notebook_login()""")

add_md("### Load FLUX.1-dev via GGUF (6GB) to avoid RAM crash")

add_code("""import torch
from huggingface_hub import hf_hub_download
from diffusers import FluxPipeline, FluxTransformer2DModel, GGUFQuantizationConfig

print("Downloading GGUF weights (6.8GB)...")
ckpt_path = hf_hub_download(
    repo_id="city96/FLUX.1-dev-gguf",
    filename="flux1-dev-Q4_K_S.gguf"
)

print("Loading GGUF transformer...")
transformer = FluxTransformer2DModel.from_single_file(
    ckpt_path,
    quantization_config=GGUFQuantizationConfig(compute_dtype=torch.bfloat16),
    torch_dtype=torch.bfloat16,
)

print("Loading FLUX pipeline... (Only downloads T5 & VAE, saves huge RAM!)")
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    transformer=transformer,
    torch_dtype=torch.bfloat16
)

# Enable memory savings for 16GB T4 GPU
pipe.enable_model_cpu_offload()
print("Pipeline loaded successfully! 🚀")
""")

add_md("### Batch Generation")

add_code("""import json
import os

# Paste your prompts generated from Phase 1 here
prompts_data = [
    {
        "id": "pooja_01",
        "prompt": "cinematic photorealistic background art for Satyanarayan Pooja, Lord Vishnu iconography, marigold and gold color palette, sacred atmosphere, hyper-realistic, banana leaves arranged in a traditional pattern, ornate brass kalash with coconut and mango leaves, glowing oil lamps (diyas) with warm flickering flames, intricate floral garlands of marigolds and jasmine, soft volumetric lighting, divine aura, intricate details, 8k resolution, shallow depth of field, no text, no typography, no logos, no banners"
    }
]

output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

import gc
gc.collect()
torch.cuda.empty_cache()

for item in prompts_data:
    print(f"Generating image for {item['id']}...")
    image = pipe(
        item['prompt'],
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=20,
        max_sequence_length=256
    ).images[0]
    
    out_path = f"{output_dir}/{item['id']}.jpg"
    image.save(out_path, quality=95)
    print(f"Saved {out_path}")
""")

add_md("### Download Results")

add_code("""import shutil
from google.colab import files

shutil.make_archive("daivbharathi_art", 'zip', output_dir)
files.download("daivbharathi_art.zip")
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
with open('notebooks/Colab_Flux_Art_Engine.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated at notebooks/Colab_Flux_Art_Engine.ipynb")
