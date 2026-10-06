import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
pkill -f main.py
sleep 1
cd /home/ubuntu/open-imggen/ComfyUI
mv comfy.log comfy.log.bak
echo "Starting ComfyUI..." > comfy.log
nohup /home/ubuntu/open-imggen/ComfyUI/venv/bin/python main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 >> comfy.log 2>&1 < /dev/null &
sleep 5
cat comfy.log
ps aux | grep main.py
"""

print("Restarting ComfyUI with explicit python path...")
stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode('utf-8'))
ssh.close()
