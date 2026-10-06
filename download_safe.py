import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
/home/ubuntu/open-imggen/ComfyUI/venv/bin/python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='unsloth/Z-Image-Turbo-FP8', filename='Z-Image-Turbo-FP8.safetensors', local_dir='.')"
"""

print("Executing download script...")
stdin, stdout, stderr = ssh.exec_command(cmds)

exit_status = stdout.channel.recv_exit_status()
print(f"Done with status {exit_status}")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
