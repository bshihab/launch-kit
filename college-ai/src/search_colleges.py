from google.cloud import firestore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FirestoreRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LangChain components
firestore_client = firestore.Client()
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
retriever = FirestoreRetriever(firestore_client, embeddings)

chat_model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Create retrieval chain
retrieval_chain = RetrievalQA.from_chain_type(
    llm=chat_model,
    retriever=retriever,
    return_source_documents=True
)

def search_colleges(query):
    """
    Search for colleges using LangChain's RetrievalQA.
    """
    response = retrieval_chain.run(query)
    return response

if __name__ == "__main__":
    query = input("Enter your query: ")
    response = search_colleges(query)
    print("\nSearch Results:")
    print(response)
