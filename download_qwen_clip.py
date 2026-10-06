import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/clip
if [ ! -f "Qwen3-4B-UD-Q6_K_XL.gguf" ]; then
    echo "Downloading Qwen3-4B CLIP for Z-Image Turbo..."
    curl -L -C - -o Qwen3-4B-UD-Q6_K_XL.gguf "https://huggingface.co/fsxedx/Z-Image-Turbo-GGUF/resolve/main/Qwen3-4B-UD-Q6_K_XL.gguf?download=true"
fi
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
for line in iter(stdout.readline, ""):
    pass
ssh.close()
