import qrcode
from PIL import Image
import sys
import os

def generate_qr(url, output_file="qrcode.png"):
    """Generate a QR code for any URL and save it as an image."""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    
    print(f"✅ QR code saved as: {output_file}")
    print(f"🔗 Encoded URL: {url}")
    print("📱 Scan with your phone to open the link!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Interactive mode if no argument is given
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
