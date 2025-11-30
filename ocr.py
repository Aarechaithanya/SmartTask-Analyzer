import pytesseract
from PIL import Image
import os

# -------------------------------------------------
# SET TESSERACT PATH (IMPORTANT: UPDATE THIS)
# -------------------------------------------------

# Windows Example Path:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Linux / Ubuntu Path:
# pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


# -------------------------------------------------
# OCR FUNCTION
# -------------------------------------------------

def extract_text(image_path):
    """
    Takes an image file path and returns extracted text using OCR.
    """

    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return "Error: File not found."

        # Open the image using PIL
        image = Image.open(image_path)

        # Convert to RGB (fixes issues with some image formats)
        image = image.convert("RGB")

        # Perform OCR
        text = pytesseract.image_to_string(image)

        # Clean output
        text = text.strip()

        if text == "":
            return "No readable text found in the input image."

        return text

    except Exception as e:
        return f"OCR Error: {str(e)}"
