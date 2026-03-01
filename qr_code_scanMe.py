import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def generate_qr(url, output_file="qrcode.png"):
    """Generate a QR code with a 'SCAN ME' label in the center."""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction (needed for center overlay)
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create the QR code image in RGBA mode for transparency support
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img_width, img_height = img.size

    # --- Create the "SCAN ME" label (two lines, no box) ---
    draw = ImageDraw.Draw(img)

    # Try to load a clean regular font, fall back to default if not available
    font_size = int(img_width * 0.09)  # Scale font relative to QR size
    try:
        font = ImageFont.truetype("arial.ttf", font_size)         # Windows
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)  # Linux
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)  # macOS
            except:
                font = ImageFont.load_default()

    line1 = "SCAN"
    line2 = "ME"
    gap = int(font_size * 0.1)  # Small gap between the two lines

    bbox1 = draw.textbbox((0, 0), line1, font=font)
    bbox2 = draw.textbbox((0, 0), line2, font=font)

    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]

    total_height = h1 + gap + h2
    padding = int(font_size * 0.4)  # White space around text to clear QR dots

    # White background rectangle to erase QR dots behind text
    block_w = max(w1, w2) + padding * 2
    block_h = total_height + padding * 2
    block_x = (img_width - block_w) // 2
    block_y = (img_height - block_h) // 2
    draw.rectangle([block_x, block_y, block_x + block_w, block_y + block_h], fill="white")

    # Draw SCAN centered
    x1 = (img_width - w1) // 2 - bbox1[0]
    y1 = block_y + padding - bbox1[1]
    draw.text((x1, y1), line1, fill="black", font=font)

    # Draw ME centered below
    x2 = (img_width - w2) // 2 - bbox2[0]
    y2 = y1 + h1 + gap
    draw.text((x2, y2), line2, fill="black", font=font)

    # Save as PNG
    img.convert("RGB").save(output_file)

    print(f"✅ QR code saved as: {output_file}")
    print(f"🔗 Encoded URL: {url}")
    print("📱 Scan with your phone to open the link!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Enter the URL/link to encode: ").strip()
        if not url:
            print("❌ No URL provided.")
            sys.exit(1)
        output = input("Enter output filename (press Enter for 'qrcode.png'): ").strip()
        output = output if output else "qrcode.png"
    else:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else "qrcode.png"

    # Add https:// if no scheme is provided
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    generate_qr(url, output)