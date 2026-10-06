#!/bin/bash
cd /home/ubuntu/open-imggen/ComfyUI
source venv/bin/activate
nohup python main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 > comfy.log 2>&1 < /dev/null &
