import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


BACKGROUND_COLORS = [
    "#4A6FA5",
    "#6B8E7B",
    "#8B6F47",
    "#7B6B8E",
    "#5C7A8A",
    "#6B7B8E",
    "#8B7B6B",
    "#5A7A6B",
]


def generate_avatar(name: str) -> ContentFile:
    letter = (name or "?")[0].upper()
    color = random.choice(BACKGROUND_COLORS)
    size = 128
    image = Image.new("RGB", (size, size), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    x = (size - (bbox[2] - bbox[0])) // 2
    y = (size - (bbox[3] - bbox[1])) // 2 - 4
    draw.text((x, y), letter, fill="white", font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
