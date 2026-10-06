import paramiko
import sys
import io

# Force utf-8 encoding for standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
tail -n 50 /home/ubuntu/open-imggen/ComfyUI/comfy.log
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode('utf-8'))
ssh.close()
