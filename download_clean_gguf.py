import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
rm -f z-image-turbo-bf16-aio.safetensors
if [ ! -f "z_image_turbo-Q5_K_S.gguf" ]; then
    echo "Downloading working Q5_K_S GGUF (Low VRAM optimized)..."
    wget -q --show-progress -O z_image_turbo-Q5_K_S.gguf "https://huggingface.co/fsxedx/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q5_K_S.gguf?download=true"
fi
"""

print("Executing clean GGUF download...")
stdin, stdout, stderr = ssh.exec_command(cmds)
exit_status = stdout.channel.recv_exit_status()
print(f"Done: {exit_status}")
ssh.close()
