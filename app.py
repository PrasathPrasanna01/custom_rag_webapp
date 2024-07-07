from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import fitz  # PyMuPDF for PDF processing
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load environment variables
load_dotenv()

# Azure Blob Storage credentials
blob_service_client = BlobServiceClient(account_url="https://yourstorageaccount.blob.core.windows.net", credential="your-blob-storage-key")

# Azure Cognitive Search credentials
search_service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
search_endpoint = f"https://{search_service_name}.search.windows.net"
credential = AzureKeyCredential(search_api_key)
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential)

# OpenAI credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def upload_document_to_blob_storage(file_path, container_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

def upload_document_to_azure_search(doc_id, content):
    document = {
        "id": doc_id,
        "content": content
    }
    result = search_client.upload_documents(documents=[document])
    return result

def ask_openai(question, context):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]

        # Check if file is selected
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        # If file exists and is valid, process it
        if file:
            # Save file to a temporary location
            file_path = os.path.join(app.root_path, "uploads", file.filename)
            file.save(file_path)

            # Extract text from PDF
            text = extract_text_from_pdf(file_path)

            # Upload document to Blob Storage
            upload_document_to_blob_storage(file_path, "your-container-name")

            # Upload extracted text to Azure Cognitive Search
            upload_document_to_azure_search(file.filename, text)

            # Ask a question using OpenAI
            question = "What is the main idea of the document?"
            answer = ask_openai(question, text)

            return render_template("index.html", filename=file.filename, text=text, question=question, answer=answer)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
