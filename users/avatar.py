import io
import random
from enum import StrEnum

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


class AvatarColor(StrEnum):
    BLUE = "#4A6FA5"
    GREEN = "#6B8E7B"
    BROWN = "#8B6F47"
    PURPLE = "#7B6B8E"
    TEAL = "#5C7A8A"
    SLATE = "#6B7B8E"
    TAN = "#8B7B6B"
    SAGE = "#5A7A6B"


BACKGROUND_COLORS = list(AvatarColor)

AVATAR_SIZE = 128
AVATAR_FONT_SIZE = AVATAR_SIZE // 2
AVATAR_ANCHOR = (0, 0)
AVATAR_TEXT_COLOR = "white"


def generate_avatar(name: str) -> ContentFile:
    letter = (name or "?")[0].upper()
    color = random.choice(BACKGROUND_COLORS)
    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default(size=AVATAR_FONT_SIZE)
    bbox = draw.textbbox(AVATAR_ANCHOR, letter, font=font)
    x = (AVATAR_SIZE - (bbox[2] - bbox[0])) // 2
    y = (AVATAR_SIZE - (bbox[3] - bbox[1])) // 2 - 4
    draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
