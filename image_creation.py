from PIL import Image, ImageDraw, ImageFont

from interpretation import Interpretation

from typing import List


def stitch_horizontal(images: List[Image.Image]) -> Image.Image:
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im

def center_and_stitch_vertical(images: List[Image.Image], vertical_padding: int = 60) -> Image.Image:
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images) + vertical_padding * (len(images) + 1)

    stitched_image = Image.new("RGB", (max_width, total_height), "white")

    y_offset = vertical_padding // 2
    for img in images:
        x_offset = (max_width - img.width) // 2
        stitched_image.paste(img, (x_offset, y_offset))
        y_offset += img.height
        y_offset += vertical_padding

    return stitched_image

def create_interpretation_image(
    interpretation: Interpretation, width: int
) -> Image.Image:
    # Load a Unicode-compatible font with logical symbols
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Prepare interpretation text
    interpretation_text = str(interpretation)
    lines = interpretation_text.splitlines()

    # Calculate image size based on text content
    line_height = font.getbbox("A")[3]  # Calculate the height of a single line
    text_height = line_height * len(lines) + 10  # Add padding
    image = Image.new("RGB", (width, text_height), "white")
    draw = ImageDraw.Draw(image)

    x_offset = max(0, (width - max(len(line) * 10 for line in lines)) // 2)

    # Draw each line of the interpretation text
    y = 5
    for line in lines:
        draw.text((x_offset, y), line, fill="black", font=font)
        y += line_height

    return image
