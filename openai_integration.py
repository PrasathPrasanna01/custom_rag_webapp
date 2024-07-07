# openai_integration.py
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(question, context):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Example usage (for testing purposes)
if __name__ == "__main__":
    question = "What is the main idea of the document?"
    context = "Example document content"  # Replace with actual document content
    answer = ask_openai(question, context)
    print(f"Question: {question}")
    print(f"Answer: {answer}")