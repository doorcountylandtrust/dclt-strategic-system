import os
from PIL import Image, ImageEnhance
import pytesseract

# === CONFIG ===
input_dir = "./"  # Change this to the directory with screenshots
output_dir = "ocr_output"
resize_factor = 2.0

# === Make sure output folder exists ===
os.makedirs(output_dir, exist_ok=True)

# === Supported extensions ===
extensions = (".png", ".jpg", ".jpeg")

# === Loop through files ===
for filename in os.listdir(input_dir):
    if filename.lower().endswith(extensions):
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")

        try:
            print(f"🔍 Processing: {filename}")

            # Load and enhance image
            img = Image.open(input_path).convert("RGB")
            img = img.resize(
                (int(img.width * resize_factor), int(img.height * resize_factor)),
                Image.LANCZOS
            )
            img = ImageEnhance.Contrast(img).enhance(1.8)
            img = ImageEnhance.Sharpness(img).enhance(2.0)

            # Run OCR
            text = pytesseract.image_to_string(img)

            # Write to file
            with open(output_path, "w") as f:
                f.write(text)

            print(f"✅ Saved OCR to: {output_path}\n")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")