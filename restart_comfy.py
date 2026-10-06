import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
# Restart ComfyUI service or kill python
pkill -f "main.py --lowvram"
sleep 2
nohup /home/ubuntu/open-imggen/ComfyUI/venv/bin/python /home/ubuntu/open-imggen/ComfyUI/main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 > /home/ubuntu/open-imggen/ComfyUI/comfy.log 2>&1 &
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
ssh.close()
print("Restarted ComfyUI")
