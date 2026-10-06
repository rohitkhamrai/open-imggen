import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
grep -A 10 "class CLIPLoaderGGUF" /home/ubuntu/open-imggen/ComfyUI/custom_nodes/ComfyUI-GGUF/nodes.py
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode())
ssh.close()
