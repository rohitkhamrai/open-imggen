import json
import os

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split('\n')]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in text.split('\n')]
    })

add_md("# DaivBharathi ComfyUI Server (Colab Edition)\nThis notebook runs the full ComfyUI Web Interface on a free Google Colab GPU (T4 16GB).\n\nIt installs the necessary GGUF nodes and downloads the required FLUX/Qwen models so you can use your exact workflow without your local PC slowing down.")

add_code("""# 0. Anti-Disconnect (Run this first to keep Colab alive!)
import IPython
from IPython.display import display, HTML

display(HTML('''
<script>
    function ConnectButton(){
        console.log("Anti-Disconnect: Ping!");
        document.querySelector("colab-connect-button").shadowRoot.querySelector("#connect").click() 
    }
    setInterval(ConnectButton, 60000);
</script>
<b style="color: green;">Anti-disconnect loop started. Colab will not kill your session due to inactivity.</b>
'''))""")

add_code("""# 1. Install ComfyUI
!git clone https://github.com/comfyanonymous/ComfyUI
%cd ComfyUI
!pip install -q -r requirements.txt""")

add_code("""# 2. Install Custom Nodes (GGUF Support)
%cd custom_nodes
!git clone https://github.com/city96/ComfyUI-GGUF
%cd ComfyUI-GGUF
!pip install -q -r requirements.txt
%cd /content/ComfyUI""")

add_code("""# 3. Download Models (Fast Downloads via aria2)
!apt-get -y install aria2

# Download Z-Image Turbo GGUF (UNet)
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/wmueller/zimgturbo/resolve/main/zimageTurboByStable_xmasQ8.gguf -d models/unet -o z_image_turbo-Q5_K_S.gguf

# Download Qwen3 GGUF (CLIP Text Encoder)
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/unsloth/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-UD-Q6_K_XL.gguf -d models/clip -o Qwen3-4B-UD-Q6_K_XL.gguf
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors -d models/clip -o clip_l.safetensors

# Download VAE
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/FLUX.1-dev/resolve/main/ae.safetensors -d models/vae -o ae.safetensors

# Download IP-Adapter Models
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors -d models/ipadapter -o ip-adapter-plus_sdxl_vit-h.safetensors
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/comfyanonymous/clip_vision_g/resolve/main/clip_vision_g.safetensors -d models/clip_vision -o clip_vision_g.safetensors
""")

add_code("""# 3.5 Install IP-Adapter Custom Node
%cd custom_nodes
!git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
%cd /content/ComfyUI
""")

add_code("""# 4. Start ComfyUI and expose it via Native Colab Proxy
import subprocess
import time
from google.colab.output import eval_js

# Start ComfyUI in the background
subprocess.Popen("python main.py --enable-cors-header > comfy_output.log 2>&1", shell=True)

# Generate the Native Colab Proxy URL
colab_url = eval_js("google.colab.kernel.proxyPort(8188)")

print(f"\\n\\033[1;32m========== COMFYUI IS STARTING ==========\\033[0m")
print(f"\\033[1;36mWait 15 seconds for the server to boot, then click this link:\\033[0m")
print(f"\\033[1;34m👉 {colab_url} 👈\\033[0m\\n")

# Tail the logs so you can see when it finishes loading
!tail -f comfy_output.log""")

notebook = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"gpuType": "T4"},
        "kernelspec": {"display_name": "Python 3", "name": "python3"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/Colab_ComfyUI_Server.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Generated notebooks/Colab_ComfyUI_Server.ipynb")
