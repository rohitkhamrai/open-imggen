import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
echo "Aggressively resuming download until complete..."
for i in {1..10}; do
    curl -L -C - -o z_image_turbo-Q5_K_S.gguf "https://huggingface.co/fsxedx/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q5_K_S.gguf?download=true"
    if [ $? -eq 0 ]; then
        echo "Download finished successfully."
        break
    fi
    echo "Download interrupted, retrying in 2 seconds..."
    sleep 2
done
ls -lh z_image_turbo-Q5_K_S.gguf
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
exit_status = stdout.channel.recv_exit_status()
print(f"Exit: {exit_status}")
print(stdout.read().decode())
ssh.close()
