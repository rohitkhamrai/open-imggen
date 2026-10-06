import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd open-imggen/ComfyUI/models/unet
if [ ! -f "zimageTurboByStable_xmasQ8.gguf" ]; then
    echo "Downloading z-img turbo GGUF..."
    wget -q --show-progress https://huggingface.co/wmueller/zimgturbo/resolve/main/zimageTurboByStable_xmasQ8.gguf -O zimageTurboByStable_xmasQ8.gguf
fi
echo "Done."
"""
print("Running download on Ubuntu...")
stdin, stdout, stderr = ssh.exec_command(cmds)
for line in iter(stdout.readline, ""):
    print(line, end="")
ssh.close()
