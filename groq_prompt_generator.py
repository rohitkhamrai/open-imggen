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

def generate_zimage_prompt(pooja_data: Dict[str, Any], api_key: str) -> str:
    """
    Parses complex Pooja JSON data and calls Groq (Llama-3) to generate a highly explicit visual prompt.
    """
    client = Groq(api_key=api_key)
    
    system_prompt = (
        "You are an expert Hindu Devotional Prompt Engineer for an advanced AI image model. "
        "Your goal is to convert abstract pooja names and spiritual descriptions into EXPLICIT, PHYSICAL, VISUAL details. "
        "AI models do not know what 'Kaal Sarp Dosh' or 'Sathyanarayana' means visually. You MUST tell them EXACTLY what to draw.\n\n"
        "CRITICAL RULES:\n"
        "1. EXTRACT RITUAL OBJECTS: Read the 'Content' and 'What's Included' data and list the exact physical objects (e.g. 'brass Kalasha with coconut and mango leaves', 'silver snake idols (Nag)', 'burning homa fire', 'black sesame seeds', 'yellow banana leaf', 'white milk offering').\n"
        "2. EXPLICIT DEITY ANATOMY: If a deity is mentioned, describe their exact physical appearance (e.g. 'Lord Shiva meditating, blue throat, snake around neck, 4 arms, holding a trishul', or 'Lord Vishnu in rich gold and maroon silk, 4 arms, holding a conch').\n"
        "3. TEXT INTEGRATION: You MUST explicitly command the AI to draw typography. Add a sentence like: 'Hovering gracefully in the blurred cinematic temple background is glowing elegant English typography that reads: \"[INSERT POOJA NAME]\" and a subtitle \"[INSERT POOJA DATE]\".'\n"
        "4. DO NOT use generic flyer layouts or solid color blocks. The text must be seamlessly integrated into the cinematic environment.\n"
        "5. Output ONLY the finalized raw paragraph prompt. No explanations, no markdown formatting."
    )
    
    # We pass the entire pooja dictionary data so the LLM can extract the deep details
    user_prompt = f"Convert this Pooja Data into a highly specific visual prompt:\n{json.dumps(pooja_data, indent=2)}"
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192",  # Using a smart Llama 3 model
            temperature=0.4,
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
        
    print(f"Generating Z-Image visual prompt for {data.get('event')}...")
    prompt = generate_zimage_prompt(data, api_key)
    
    print("\n--- GENERATED Z-IMAGE PROMPT ---")
    print(prompt)
    print("-----------------------------\n")
