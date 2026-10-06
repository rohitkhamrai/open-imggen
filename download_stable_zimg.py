import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
if [ ! -f "z_image_turbo_fp8.safetensors" ]; then
    echo "Downloading stable Z-Image-Turbo FP8..."
    wget -q --show-progress -O z_image_turbo_fp8.safetensors "https://huggingface.co/unsloth/Z-Image-Turbo-FP8/resolve/main/z_image_turbo_fp8.safetensors?download=true"
fi
"""

print("Executing download script...")
stdin, stdout, stderr = ssh.exec_command(cmds)
# Read outputs
for line in iter(stdout.readline, ""):
    sys.stdout.write(line)
for line in iter(stderr.readline, ""):
    sys.stderr.write(line)

exit_status = stdout.channel.recv_exit_status()
print(f"Done with status {exit_status}")
ssh.close()
