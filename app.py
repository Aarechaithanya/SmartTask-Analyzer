from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import spacy
import os
import uuid


# -------------------------
# INITIALIZATION
# -------------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Set Tesseract Path (UPDATE this path for your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------------------------
# OCR FUNCTION
# -------------------------

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error during OCR: {str(e)}"


# -------------------------
# SUMMARIZATION FUNCTION
# -------------------------

def summarize_text(text, max_sentences=3):
    doc = nlp(text)
    sentences = list(doc.sents)

    if not sentences:
        return "No text available for summarization."

    # Basic summarization: take important sentences
    summary = " ".join([sent.text for sent in sentences[:max_sentences]])
    return summary


# -------------------------
# API: PROCESS IMAGE
# -------------------------

@app.route("/process", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, file_id + ".jpg")
    file.save(file_path)

    # OCR
    extracted_text = extract_text(file_path)

    # Summarization
    summary = summarize_text(extracted_text)

    return jsonify({
        "status": "success",
        "extracted_text": extracted_text,
        "summary": summary
    })


# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
