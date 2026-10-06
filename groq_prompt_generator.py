import json
import os
from typing import Dict, Any

# Ensure Groq library is installed: pip install groq python-dotenv
try:
    from groq import Groq
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'groq' or 'python-dotenv' library not found. Run 'pip install groq python-dotenv'")
    exit(1)

def generate_flux_prompt(pooja_data: Dict[str, Any], api_key: str) -> str:
    """
    Parses Pooja JSON data and calls Groq Llama-3.3-70B to generate a text-free visual prompt.
    """
    client = Groq(api_key=api_key)
    
    system_prompt = (
        "You are an expert AI prompt engineer specializing in Hindu sacred iconography and photorealism. "
        "Your task is to convert event details into a highly detailed visual prompt for the FLUX.1-Dev image model. "
        "CRITICAL RULES:\n"
        "1. DO NOT include any text, typography, letters, logos, or banners in the image.\n"
        "2. Focus entirely on background art, lighting, atmosphere, and sacred items.\n"
        "3. Output ONLY the raw prompt string, nothing else. No markdown, no explanations."
    )
    
    user_prompt = (
        f"Generate a cinematic, photorealistic background art prompt for a {pooja_data.get('event', 'Pooja')} event. "
        f"Deity focus: {pooja_data.get('deity', 'None')}. "
        f"Theme: {pooja_data.get('theme_color', 'traditional')}. "
        f"Elements to include: {', '.join(pooja_data.get('key_elements', []))}. "
        f"Mood: {pooja_data.get('mood', 'sacred')}. "
        "Remember: ZERO text in the image."
    )
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="qwen/qwen3.8-27b",
            temperature=0.3,
            max_completion_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"

if __name__ == "__main__":
    load_dotenv()
    # Check for API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        print("Please set it: $env:GROQ_API_KEY='your_key'")
        exit(1)
        
    json_path = "sample_pooja.json"
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        exit(1)
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    print(f"Generating prompt for {data.get('event')}...")
    prompt = generate_flux_prompt(data, api_key)
    
    print("\n--- GENERATED FLUX PROMPT ---")
    print(prompt)
    print("-----------------------------\n")
