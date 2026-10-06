import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
# Delete old models
cd /home/ubuntu/open-imggen/ComfyUI/models/unet
rm -f zimageTurboByStable_xmasQ8.gguf

cd /home/ubuntu/open-imggen/ComfyUI/models/checkpoints
rm -f z-image-turbo-bf16-aio.safetensors
rm -f z-image-turbo-bf16-aio.safetensors.1

echo "Deleted corrupted/huge models."

# Check size of currently downloading model
echo "Current Q5_K_S download size:"
ls -lh /home/ubuntu/open-imggen/ComfyUI/models/unet/z_image_turbo-Q5_K_S.gguf
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode())
ssh.close()
