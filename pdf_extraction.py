from PyPDF2 import PdfReader
# from pdfminer.high_level import extract_text

# def extract_text_from_pdf(pdf_path):
#     text = extract_text(pdf_path)
#     return text

pdf_path = 'downloaded_pdfs/Japanese_-_Units_1-4.pdf'  # Update this path
#text = extract_text_from_pdf(pdf_path)
#print(text)


# Path to the uploaded PDF
# pdf_path = '/mnt/data/Japanese_-_Units_1-4.pdf'

# Initialize PDF reader and variables for analysis
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
text_samples = []

# Extract text from the first few pages to understand the structure
for page_num in range(min(5, num_pages)):  # Limit to first 5 pages or total page count
    page = reader.pages[page_num]
    text = page.extract_text()
    text_samples.append(f"Page {page_num + 1}:\n{text}\n{'-'*80}\n")

# Joining samples for display
text_sample_output = "\n".join(text_samples)
print(text_sample_output)


