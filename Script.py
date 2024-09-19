import pdfplumber

# Open the PDF file
with pdfplumber.open("data/1.pdf") as pdf:
    # Iterate through all pages
    for page in pdf.pages:
        # Extract text from the page
        text = page.extract_text()
        print(text)