import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
killall -9 python || true
cd /home/ubuntu/open-imggen/ComfyUI
rm comfy.log
nohup /home/ubuntu/open-imggen/ComfyUI/venv/bin/python main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 > comfy.log 2>&1 < /dev/null &
sleep 5
tail -n 30 comfy.log
"""

print("Executing fix...")
stdin, stdout, stderr = ssh.exec_command(cmds)
# Wait for command to finish
exit_status = stdout.channel.recv_exit_status()
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))
ssh.close()
