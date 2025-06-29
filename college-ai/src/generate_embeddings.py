from google.cloud import firestore
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Firestore client
firestore_client = firestore.Client()

# Initialize LangChain embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def add_embeddings_to_firestore():
    """
    Fetch college data from Firestore, generate embeddings, and store them back in Firestore.
    """
    colleges_ref = firestore_client.collection('colleges')
    docs = colleges_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        if 'school.name' not in data or 'school.city' not in data or 'school.state' not in data:
            print(f"Skipping document {doc.id}: Missing required fields.")
            continue

        # Create a description for the embedding
        description = f"{data['school.name']} in {data['school.city']}, {data['school.state']}."
        embedding = embeddings.embed_query(description)

        # Add the embedding back into Firestore
        colleges_ref.document(doc.id).update({"embedding": embedding})
        print(f"Added embedding for {data['school.name']} (ID: {doc.id})")

if __name__ == "__main__":
    add_embeddings_to_firestore()
