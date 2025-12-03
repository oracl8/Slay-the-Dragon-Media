from PIL import Image
import requests
from io import BytesIO
import urllib.parse

# Base URL
base_url = "https://raw.githubusercontent.com/oracl8/Slay-the-Dragon-Media/main/END_USER_DRAGON_LORD_BASIC/Spritesheets/"

# Define sprite sheets
sprite_sheets = {
    "dragon_lord_death_160x160.png": {"frames": 36, "prefix": "dragon_death"},
    "dragon_lord_idle_basic_74x74.png": {"frames": 4, "prefix": "dragon_idle"}
}

for filename, config in sprite_sheets.items():
    print(f"Processing {filename}...")
    
    # Download the image
    url = base_url + urllib.parse.quote(filename)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"  ✗ Failed to download")
        continue
    
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
        frame.save(f"{config['prefix']}_{i+1:02d}.png")
    
    print(f"  ✓ Saved {config['frames']} frames")

print("\nAll done!")