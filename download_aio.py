import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/checkpoints
if [ ! -f "z-image-turbo-bf16-aio.safetensors" ]; then
    echo "Downloading AIO Z-Image Turbo checkpoint..."
    wget -q --show-progress -O z-image-turbo-bf16-aio.safetensors "https://huggingface.co/RunningHubAI/rh-z-image-turbo-bf16-aio-checkpoint/resolve/main/z-image-turbo-bf16-aio.safetensors?download=true"
fi
"""

print("Executing download...")
stdin, stdout, stderr = ssh.exec_command(cmds)
exit_status = stdout.channel.recv_exit_status()
print(f"Done: {exit_status}")
ssh.close()
