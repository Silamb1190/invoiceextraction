from flask import Flask, render_template, request, jsonify
import os
import PyPDF2  # For PDF processing

app = Flask(__name__)

# Set the upload folder for PDFs
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow only PDFs to be uploaded
ALLOWED_EXTENSIONS = {'pdf'}

# Helper function to check if the file is a PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Handle PDF file upload
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdfUpload' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['pdfUpload']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and allowed_file(file.filename):
        # Save the file to the server
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Extract text from the PDF file
        invoice_details = extract_text_from_pdf(filename)
        
        return jsonify(invoice_details)
    else:
        return jsonify({"error": "Invalid file format, only PDF allowed"})

# Function to extract text from the PDF (you can improve this for better parsing)
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()
    
    # Simulate extracting invoice details from the text
    details = {
        "invoice_number": "Not Found",
        "invoice_date": "Not Found",
        "vendor_name": "Not Found",
        "vendor_address": "Not Found"
    }

    # Dummy logic to extract fields (adjust with actual text parsing logic)
    if "Invoice Number" in text:
        details["invoice_number"] = "12345"
    if "Invoice Date" in text:
        details["invoice_date"] = "2024-12-01"
    if "Vendor Name" in text:
        details["vendor_name"] = "ABC Corp"
    if "Vendor Address" in text:
        details["vendor_address"] = "123 Vendor St, City, Country"

    return details

if __name__ == '__main__':
    app.run(debug=True)
