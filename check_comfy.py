import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

print("Fetching ComfyUI log...")
stdin, stdout, stderr = ssh.exec_command('tail -n 50 /home/ubuntu/open-imggen/ComfyUI/comfy.log')
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))

print("Checking if python is running...")
stdin, stdout, stderr = ssh.exec_command('ps aux | grep main.py')
print(stdout.read().decode('utf-8'))
ssh.close()
