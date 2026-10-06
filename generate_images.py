import os
import urllib.request
import urllib.parse
import json
import time

# You can easily read this from the output of Phase 1 later.
# For now, we'll hardcode the prompt we got from the Groq API.
prompts_data = [
    {
        "id": "pooja_01",
        "prompt": "cinematic photorealistic background art for Satyanarayan Pooja, Lord Vishnu iconography, marigold and gold color palette, sacred atmosphere, hyper-realistic, banana leaves arranged in a traditional pattern, ornate brass kalash with coconut and mango leaves, glowing oil lamps (diyas) with warm flickering flames, intricate floral garlands of marigolds and jasmine, soft volumetric lighting, divine aura, intricate details, 8k resolution, shallow depth of field, no text, no typography, no logos, no banners"
    }
]

output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

print("Ponytail Mode Engaged: Generating images via free API instead of local GPU...")

for item in prompts_data:
    print(f"Generating image for {item['id']}...")
    
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(item['prompt'])
    
    # We specify model=flux and dimensions
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1024&height=1024&seed={int(time.time())}&nologo=true"
    
    out_path = os.path.join(output_dir, f"{item['id']}.jpg")
    
    try:
        # Download the image directly
        urllib.request.urlretrieve(url, out_path)
        print(f"Saved beautifully generated image to: {out_path}")
    except Exception as e:
        print(f"Failed to generate {item['id']}: {e}")

print("Phase 2 complete in 10 seconds. No Colab required.")
