import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

# Create directory
stdin, stdout, stderr = ssh.exec_command('mkdir -p /home/ubuntu/open-imggen/ComfyUI/custom_nodes/ComfyUI-NoLlama-Agent')
stdout.read() # block until mkdir finishes

# Node code
node_py = """
import requests
import torch

class NoLlamaAgent:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "nollama_api_url": ("STRING", {"default": "http://YOUR_LAPTOP_IP:11434/v1"}),
                "model_name": ("STRING", {"default": "llama3.2-vision"}),
                "user_prompt": ("STRING", {"multiline": True, "default": "Analyze the image and tell me the x, y, width, height for placing a deity."}),
                "image": ("IMAGE", ),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("enhanced_prompt", "x", "y", "width", "height")
    FUNCTION = "analyze"
    CATEGORY = "Agentic"

    def analyze(self, nollama_api_url, model_name, user_prompt, image):
        # Extremely simplified logic for Ponytail implementation
        # For actual vision analysis, we would base64 encode the tensor and send to NoLlama
        # Returning dummy coordinates and prompt to complete the graph for now
        # until the user confirms NoLlama is responding.
        try:
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": user_prompt}],
                "max_tokens": 100
            }
            res = requests.post(f"{nollama_api_url}/chat/completions", json=payload, timeout=5)
            if res.status_code == 200:
                text = res.json()["choices"][0]["message"]["content"]
            else:
                text = f"API Error: {res.status_code}"
        except Exception as e:
            text = f"Connection Error to {nollama_api_url}. Is NoLlama running?"

        return (f"{user_prompt} - {text}", 256, 256, 512, 512)

NODE_CLASS_MAPPINGS = {
    "NoLlamaAgent": NoLlamaAgent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NoLlamaAgent": "NoLlama Vision Agent"
}
"""

init_py = """
from .node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
"""

sftp = ssh.open_sftp()
with sftp.file('/home/ubuntu/open-imggen/ComfyUI/custom_nodes/ComfyUI-NoLlama-Agent/node.py', 'w') as f:
    f.write(node_py)
with sftp.file('/home/ubuntu/open-imggen/ComfyUI/custom_nodes/ComfyUI-NoLlama-Agent/__init__.py', 'w') as f:
    f.write(init_py)
sftp.close()

# Restart ComfyUI
ssh.exec_command('pkill -f main.py')
ssh.exec_command('cd ~/open-imggen/ComfyUI && source venv/bin/activate && nohup python main.py --lowvram --fp32-vae --disable-cuda-malloc --listen 0.0.0.0 --port 8188 > comfy.log 2>&1 < /dev/null &')
ssh.close()
print("Custom Node deployed and ComfyUI restarted.")
