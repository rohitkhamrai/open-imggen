import paramiko

print('Connecting to Ubuntu...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

print('Starting Local ComfyUI...')
ssh.exec_command('pkill -f "python main.py"')
ssh.exec_command('cd ~/open-imggen && nohup bash start.sh > comfy.log 2>&1 &')
ssh.close()
print('Local ComfyUI is booting up! It may take 15 seconds to become available at http://192.168.0.134:8188')
