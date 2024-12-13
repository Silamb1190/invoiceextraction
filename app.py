import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define the upload folder for the PDF files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle PDF file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(filepath)
    
    # Return the extracted text as JSON
    return jsonify({'text': extracted_text})

# Function to extract text from a PDF using PyMuPDF
def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    extracted_text = ""
    
    # Extract text from all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        extracted_text += page.get_text("text") + "\n"
    
    return extracted_text

if __name__ == '__main__':
    app.run(debug=True)
