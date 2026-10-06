import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/custom_nodes

if [ ! -d "ComfyUI-GGUF" ]; then
    echo "Cloning ComfyUI-GGUF..."
    git clone https://github.com/city96/ComfyUI-GGUF
fi

cd ComfyUI-GGUF
/home/ubuntu/open-imggen/ComfyUI/venv/bin/pip install -r requirements.txt || /home/ubuntu/open-imggen/ComfyUI/venv/bin/pip install gguf

echo "Restarting ComfyUI..."
pkill -f main.py
cd /home/ubuntu/open-imggen/ComfyUI
source venv/bin/activate
nohup python main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 > comfy.log 2>&1 < /dev/null &
echo "Done."
"""

print("Installing GGUF Node and restarting server...")
stdin, stdout, stderr = ssh.exec_command(cmds)
for line in iter(stdout.readline, ""):
    print(line, end="")
ssh.close()
