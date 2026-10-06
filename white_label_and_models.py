import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
# 1. White-label ComfyUI to DaivBharathi AI
cd /home/ubuntu/open-imggen/ComfyUI/web
sed -i 's/<title>ComfyUI/<title>DaivBharathi AI/g' index.html

# 2. Download pure SDXL VAE and CLIPs to avoid using Juggernaut
cd /home/ubuntu/open-imggen/ComfyUI/models/vae
if [ ! -f "sdxl_vae.safetensors" ]; then
    echo "Downloading pure SDXL VAE..."
    wget -q --show-progress https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors -O sdxl_vae.safetensors
fi

cd ../clip
if [ ! -f "clip_g.safetensors" ]; then
    echo "Downloading CLIP G..."
    wget -q --show-progress https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors -O clip_g.safetensors
fi

if [ ! -f "clip_l.safetensors" ]; then
    echo "Downloading CLIP L..."
    wget -q --show-progress https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors -O clip_l.safetensors
fi
echo "Done."
"""

print("Running white-labeling and fresh model downloads on Ubuntu...")
stdin, stdout, stderr = ssh.exec_command(cmds)
for line in iter(stdout.readline, ""):
    print(line, end="")
ssh.close()
