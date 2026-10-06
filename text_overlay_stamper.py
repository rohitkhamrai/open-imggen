import json
import os
from PIL import Image, ImageDraw, ImageFont

def stamp_text_on_image(image_path, json_path, output_path):
    """
    Layer 2: The Text Stamper
    Reads the pristine generated background image and stamps the English text
    (Pooja Name, Date, Venue) beautifully on top, ensuring zero spelling errors.
    """
    if not os.path.exists(image_path):
        print(f"Error: Could not find image at {image_path}")
        return
    if not os.path.exists(json_path):
        print(f"Error: Could not find JSON data at {json_path}")
        return

    # Load the JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Load the background image
    img = Image.open(image_path).convert("RGBA")
    
    # Create an overlay layer for the dark gradient/banner at the bottom
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    width, height = img.size
    
    # Draw a semi-transparent dark gradient at the bottom so text is readable
    # (Simulating a premium banner overlay)
    banner_height = int(height * 0.35)
    for y in range(height - banner_height, height):
        alpha = int((y - (height - banner_height)) / banner_height * 230)
        draw.line([(0, y), (width, y)], fill=(20, 10, 5, alpha))
        
    # Merge overlay with original image
    img = Image.alpha_composite(img, overlay)
    
    # Initialize text drawing
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font (Fallback to default if not found)
    try:
        # Standard Windows fonts that look clean
        title_font = ImageFont.truetype("georgia.ttf", int(width * 0.055))
        subtitle_font = ImageFont.truetype("arial.ttf", int(width * 0.035))
        brand_font = ImageFont.truetype("arialbd.ttf", int(width * 0.025))
    except IOError:
        # Fallback if fonts don't exist
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # Get data from JSON
    title_text = data.get('event', 'Sacred Pooja').upper()
    date_text = f"Date: {data.get('date', '')} | Time: {data.get('time', '')}"
    venue_text = data.get('venue', 'DaivBharathi')
    brand_text = "DAIV BHARATHI - TRUSTED BY DEVOTEES"
    
    # Helper to calculate text width/height
    def draw_centered_text(text, font, y_pos, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        x_pos = (width - text_w) / 2
        
        # Add slight drop shadow for absolute premium readability
        draw.text((x_pos + 2, y_pos + 2), text, font=font, fill=(0, 0, 0, 200))
        draw.text((x_pos, y_pos), text, font=font, fill=color)

    # Draw the text at the bottom banner
    start_y = height - banner_height + int(height * 0.05)
    draw_centered_text(title_text, title_font, start_y, (255, 215, 0)) # Gold Title
    
    start_y += int(height * 0.07)
    draw_centered_text(date_text, subtitle_font, start_y, (255, 255, 255)) # White Subtitle
    
    start_y += int(height * 0.05)
    draw_centered_text(venue_text, subtitle_font, start_y, (220, 220, 220)) # Light Gray Venue
    
    # Draw Brand Tag at the very bottom
    draw_centered_text(brand_text, brand_font, height - int(height * 0.06), (200, 50, 50)) # Red Brand

    # Convert back to RGB for saving as JPG
    final_img = img.convert("RGB")
    
    # Resize to the strict 600x600px requested in the ChatGPT prompt!
    final_img = final_img.resize((600, 600), Image.Resampling.LANCZOS)
    
    final_img.save(output_path, quality=90, optimize=True)
    print(f"\\n[SUCCESS] Saved premium stamped image to: {output_path}")
    print("File size is strictly optimized for web (<1MB) at 600x600px.")

if __name__ == "__main__":
    # Test execution
    test_image = "test_pooja.jpg" # Make sure to have a dummy image here
    json_data = "sample_pooja.json"
    output = "final_website_asset.jpg"
    
    print("Layer 2: Initializing Text Stamper...")
    stamp_text_on_image(test_image, json_data, output)
