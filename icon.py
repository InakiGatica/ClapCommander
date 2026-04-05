from PIL import Image, ImageDraw, ImageFont


def create_icon_file(path="icon.ico"):
    """Generate a clap detector icon with clap emoji style."""
    # Create 256x256 image with dark background
    img = Image.new("RGB", (256, 256), color="#1a1a1a")
    draw = ImageDraw.Draw(img)

    # Dark circle background
    draw.ellipse((10, 10, 246, 246), fill="#2c2c2c", outline="#e74c3c", width=6)

    # Draw clap emoji text "👏"
    try:
        font = ImageFont.truetype("seguiemj.ttf", 120)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()

    # Center the emoji
    text = "👏"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (256 - text_width) // 2
    y = (256 - text_height) // 2

    draw.text((x, y), text, font=font)

    # Save as .ico with multiple sizes
    sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    icon_images = []
    for size in sizes:
        icon_images.append(img.resize(size, Image.LANCZOS))

    icon_images[0].save(
        path,
        format="ICO",
        sizes=sizes,
        append_images=icon_images[1:]
    )

    print(f"{path} created!")


if __name__ == "__main__":
    create_icon_file()