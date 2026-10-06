import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.134', username='ubuntu', password='Daikin@2026')

cmds = """
cat << 'EOF' > /home/ubuntu/open-imggen/ComfyUI/custom_nodes/ComfyUI-NoLlama-Agent/node.py
import requests
import torch

class NoLlamaTextEnhancer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "nollama_api_url": ("STRING", {"default": "http://192.168.0.10:11434/v1"}),
                "model_name": ("STRING", {"default": "llama3.2"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a prompt engineer for an Indian Yajna card generator. Translate the user's broken text into highly detailed, visually descriptive English for an AI image generator. Only output the final prompt, nothing else."}),
                "base_style": ("STRING", {"multiline": True, "default": "Beautiful Yajna invitation card, glowing fire, marigold garlands, highly detailed, 8k, pooja decoration, intricate borders."}),
                "user_input": ("STRING", {"multiline": True, "default": "ganesh pooja with lots of flowers"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "enhance"
    CATEGORY = "Agentic"

    def enhance(self, nollama_api_url, model_name, system_prompt, base_style, user_input):
        try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User Input: {user_input}"}
                ],
                "max_tokens": 150
            }
            res = requests.post(f"{nollama_api_url}/chat/completions", json=payload, timeout=10)
            if res.status_code == 200:
                enhanced_text = res.json()["choices"][0]["message"]["content"].strip()
            else:
                enhanced_text = user_input
        except Exception as e:
            enhanced_text = user_input
            
        final_prompt = f"{base_style}, {enhanced_text}"
        return (final_prompt,)

NODE_CLASS_MAPPINGS = {
    "NoLlamaTextEnhancer": NoLlamaTextEnhancer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NoLlamaTextEnhancer": "NoLlama Prompt Enhancer"
}
EOF
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
print(stdout.read().decode())
ssh.close()
