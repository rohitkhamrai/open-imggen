import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
killall wget || true
echo "Resuming download..."
curl -L -C - -o z_image_turbo-Q5_K_S.gguf "https://huggingface.co/fsxedx/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q5_K_S.gguf?download=true"
"""

print("Executing curl resume...")
stdin, stdout, stderr = ssh.exec_command(cmds)
exit_status = stdout.channel.recv_exit_status()
print(f"Done: {exit_status}")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
