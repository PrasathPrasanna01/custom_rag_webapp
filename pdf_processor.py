# pdf_processor.py
import fitz  # PyMuPDF for PDF processing

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

# Example usage (for testing purposes)
if __name__ == "__main__":
    pdf_path = "path/to/your/document.pdf"  # Replace with your PDF file path
    text = extract_text_from_pdf(pdf_path)
    print(text)  # Or save 'text' for further processing