import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
echo "=== PROCESSES ==="
ps aux | grep main.py

echo "\n=== PORT 8188 ==="
sudo netstat -tulpn | grep 8188

echo "\n=== COMFY LOG END ==="
tail -n 50 /home/ubuntu/open-imggen/ComfyUI/comfy.log
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))
ssh.close()
