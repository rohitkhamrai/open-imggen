import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

stdin, stdout, stderr = ssh.exec_command("find /home/ubuntu/open-imggen/ComfyUI/custom_nodes -name '*.py' | xargs grep -Hn 'TextEncodeQwenImage21'")
print(stdout.read().decode())
