# azure_search.py
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Cognitive Search credentials
search_service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
search_endpoint = f"https://{search_service_name}.search.windows.net"
credential = AzureKeyCredential(search_api_key)
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential)

def upload_document(doc_id, content):
    document = {
        "id": doc_id,
        "content": content
    }
    result = search_client.upload_documents(documents=[document])
    return result

# Example usage (for testing purposes)
if __name__ == "__main__":
    doc_id = "1"
    content = "Example document content"  # Replace with actual content or extracted text
    upload_document(doc_id, content)