from PIL import Image, ImageDraw, ImageFont
import textwrap

from interpretation import Interpretation
from constants import CAPTION_FONT, TITLE_CONTENT_FONT, CAPTION_FONT_BOLD

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


def center_and_stitch_vertical(
    images: List[Image.Image], vertical_padding: int = 60
) -> Image.Image:
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images) + vertical_padding * (
        len(images) + 1
    )

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
        font = ImageFont.truetype(*TITLE_CONTENT_FONT)
    except IOError:
        font = ImageFont.load_default()

    # Prepare interpretation text and split it into sections
    interpretation_text = str(interpretation)
    sections = interpretation_text.split(
        "\n\n"
    )  # Separate each section by double newline
    wrapped_sections = [
        wrap_text_with_newlines(section, width // 40) for section in sections
    ]

    # Set up column width and spacing
    num_columns = 4
    column_width = width // num_columns
    column_spacing = 16
    line_height = font.getbbox("A")[3]
    section_spacing = 10  # Vertical space between sections in the same column

    # Calculate positions for each section
    positions = []
    y_offsets = [0] * num_columns  # Track vertical position for each column

    for i, section in enumerate(wrapped_sections):
        column = i % num_columns  # Determine which column to place this section
        x_offset = column * (
            column_width + column_spacing
        )  # Horizontal position based on column

        # Record positions of each line in the section for this column
        for line in section:
            positions.append((line, x_offset, y_offsets[column]))
            y_offsets[column] += line_height

        # Add spacing after the section within the same column
        y_offsets[column] += section_spacing

    # Calculate total image height and width
    total_height = max(y_offsets) + 20  # Height based on tallest column, with padding
    total_width = (
        width + column_spacing
    )  # Add minimal padding to ensure fit within width
    border_size = 10  # Size of the outer border padding around the content
    inner_padding = 10  # Padding between the border and the content

    # Create an image with space for the border and inner padding
    image = Image.new(
        "RGB",
        (
            total_width + 2 * border_size + 2 * inner_padding,
            total_height + 2 * border_size + 2 * inner_padding,
        ),
        "white",
    )
    draw = ImageDraw.Draw(image)

    # Draw a border around the image with specified padding
    border_color = "black"
    draw.rectangle(
        [
            border_size - 1,
            border_size - 1,
            image.width - border_size,
            image.height - border_size,
        ],
        outline=border_color,
        width=2,
    )

    # Draw each line at its calculated position, shifted inward by border and inner padding
    for line, x, y in positions:
        draw.text(
            (x + border_size + inner_padding, y + border_size + inner_padding),
            line,
            fill="black",
            font=font,
        )

    return image


def wrap_text_with_newlines(text, width):
    wrapped_lines = []
    for line in text.splitlines():  # Split on existing newlines
        wrapped_lines.extend(
            textwrap.wrap(line, width=width) or [""]
        )  # Wrap each line separately
    return wrapped_lines

def add_caption_below_image(
    image: Image.Image, caption: str, level_count: int = 10
) -> Image.Image:
    # Load fonts with logical symbols support
    try:
        font = ImageFont.truetype(*CAPTION_FONT)  # Regular font for body
        bold_font = ImageFont.truetype(*CAPTION_FONT_BOLD)  # Bold font for first line
    except IOError:
        font = ImageFont.load_default()  # Fallback if the TTF font is not found
        bold_font = font

    max_width = image.width  # Max width for line wrapping

    # Wrap text to fit within the max width
    draw = ImageDraw.Draw(image)
    lines = wrap_text_with_newlines(caption, width=max_width // (level_count * 2))

    # Calculate total height for all lines using textbbox
    line_height = draw.textbbox((0, 0), "A", font=font)[3]  # Height of a single line
    total_text_height = line_height * len(lines) + 10  # Add padding

    # Create a new image with extra height for the caption
    total_height = image.height + total_text_height
    annotated_image = Image.new("RGB", (image.width, total_height), "white")

    # Paste the original image on top
    annotated_image.paste(image, (0, 0))

    # Draw each line of wrapped text below the image
    draw = ImageDraw.Draw(annotated_image)
    y_text = image.height + 5
    for i, line in enumerate(lines):
        # Use bold font for the first line and regular font for the rest
        current_font = bold_font if i == 0 else font
        text_width = draw.textbbox((0, 0), line, font=current_font)[2]  # Get width of each line
        draw.text(
            ((image.width - text_width) // 2, y_text), line, fill="black", font=current_font
        )
        y_text += line_height

    return annotated_image
