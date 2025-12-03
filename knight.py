from PIL import Image
import requests
from io import BytesIO
import urllib.parse

# Base URL
base_url = "https://raw.githubusercontent.com/oracl8/Slay-the-Dragon-Media/main/Sprites/without_outline/"

# Define all sprite sheets with their configurations
sprite_sheets = {
    "ATTACK 1.png": {"frames": 6, "width": 576, "prefix": "attack1"},
    "ATTACK 2.png": {"frames": 5, "width": 480, "prefix": "attack2"},
    "ATTACK 3.png": {"frames": 6, "width": 576, "prefix": "attack3"},
    "IDLE.png": {"frames": 7, "width": 672, "prefix": "idle"},
    "WALK.png": {"frames": 8, "width": 768, "prefix": "walk"},
    "RUN.png": {"frames": 8, "width": 768, "prefix": "run"},
    "JUMP.png": {"frames": 5, "width": 480, "prefix": "jump"},
    "DEFEND.png": {"frames": 6, "width": 576, "prefix": "defend"},
    "HURT.png": {"frames": 4, "width": 384, "prefix": "hurt"},
    "DEATH.png": {"frames": 12, "width": 1152, "prefix": "death"}
}

for filename, config in sprite_sheets.items():
    print(f"Processing {filename}...")
    
    # Download the image (properly encode URL)
    url = base_url + urllib.parse.quote(filename)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"  ✗ Failed to download")
        continue
    
    try:
        sheet = Image.open(BytesIO(response.content))
        sheet_width, sheet_height = sheet.size
        
        # Calculate frame dimensions
        frame_width = sheet_width // config["frames"]
        frame_height = sheet_height
        
        print(f"  Sheet size: {sheet_width}x{sheet_height}")
        print(f"  Frame size: {frame_width}x{frame_height}")
        
        # Extract frames horizontally
        for i in range(config["frames"]):
            left = i * frame_width
            top = 0
            right = left + frame_width
            bottom = frame_height
            
            frame = sheet.crop((left, top, right, bottom))
            frame.save(f"knight_{config['prefix']}_{i+1:02d}.png")
        
        print(f"  ✓ Saved {config['frames']} frames")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\nAll done!")