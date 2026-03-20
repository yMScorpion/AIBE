import os
from PIL import Image, ImageDraw

def create_tv(path):
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw stand
    draw.rectangle([12, 28, 20, 31], fill=(100, 100, 100, 255))
    # Draw screen outline
    draw.rectangle([2, 8, 30, 28], fill=(50, 50, 50, 255))
    # Draw screen inner
    draw.rectangle([4, 10, 28, 26], fill=(10, 10, 40, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

def create_pool_table(path):
    img = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw legs
    draw.rectangle([2, 40, 6, 48], fill=(101, 67, 33, 255))
    draw.rectangle([26, 40, 30, 48], fill=(101, 67, 33, 255))
    # Draw table
    draw.rectangle([0, 10, 32, 42], fill=(101, 67, 33, 255)) # Brown edge
    draw.rectangle([2, 12, 30, 40], fill=(0, 128, 0, 255)) # Green felt
    # Draw pockets
    draw.ellipse([0, 10, 6, 16], fill=(0, 0, 0, 255))
    draw.ellipse([26, 10, 32, 16], fill=(0, 0, 0, 255))
    draw.ellipse([0, 24, 6, 30], fill=(0, 0, 0, 255))
    draw.ellipse([26, 24, 32, 30], fill=(0, 0, 0, 255))
    draw.ellipse([0, 36, 6, 42], fill=(0, 0, 0, 255))
    draw.ellipse([26, 36, 32, 42], fill=(0, 0, 0, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

def create_ping_pong(path):
    img = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw legs
    draw.rectangle([4, 40, 6, 48], fill=(150, 150, 150, 255))
    draw.rectangle([26, 40, 28, 48], fill=(150, 150, 150, 255))
    # Draw table
    draw.rectangle([0, 10, 32, 42], fill=(20, 80, 180, 255)) # Blue table
    # Draw white lines
    draw.rectangle([1, 11, 31, 41], outline=(255, 255, 255, 255), width=1)
    draw.rectangle([15, 11, 16, 41], fill=(255, 255, 255, 255)) # center line
    # Draw net
    draw.rectangle([-2, 25, 34, 27], fill=(200, 200, 200, 255))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

base1 = "c:/Users/ADRIANO/AIDA/aibe/ui/frontend/public/pixel-agents/assets/furniture/"
base2 = "c:/Users/ADRIANO/AIDA/pixel-agents/webview-ui/public/assets/furniture/"

for base in [base1, base2]:
    create_tv(os.path.join(base, "TV", "TV.png"))
    create_pool_table(os.path.join(base, "POOL_TABLE", "POOL_TABLE.png"))
    create_ping_pong(os.path.join(base, "PING_PONG", "PING_PONG.png"))

print("Assets created successfully.")
