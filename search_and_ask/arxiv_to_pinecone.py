# arxiv_to_pinecone.py

from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from langchain.llms import HuggingFaceEndpoint
from langchain.chains import RetrievalQA

from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

import requests
import fitz  # PyMuPDF
import feedparser
from urllib.parse import quote
from io import BytesIO
from uuid import uuid4
import getpass
import os
import time

# Load environment variables
load_dotenv()

# -------------------- Helper Functions --------------------

def extract_text_from_pdf_url(pdf_url):
    """Download and extract text from a PDF URL."""
    response = requests.get(pdf_url)
    with fitz.open("pdf", BytesIO(response.content)) as doc:
        return "\n".join(page.get_text() for page in doc)

def connect_to_pinecone():
    """Connect to Pinecone and ensure index exists."""
    if not os.getenv("PINECONE_API_KEY"):
        os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")

    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "rpapers"

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    print("📚 Existing Pinecone Indexes:", existing_indexes)

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=os.environ["PINECONE_ENV"])
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(index_name)

def setup_embeddings_and_chunks(url):
    """Setup embeddings and split PDF text into chunks."""
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
    text = extract_text_from_pdf_url(url)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=240)
    chunks = splitter.create_documents([text])
    return embeddings, chunks

def add_to_vector_store(index, embeddings, chunks):
    """Add document chunks to Pinecone vectorstore."""
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    documents = [Document(page_content=chunk.page_content, metadata={"source": "arxiv"}) for chunk in chunks]
    uuids = [str(uuid4()) for _ in documents]
    vector_store.add_documents(documents=documents, ids=uuids)
    return vector_store

def query_llm(vector_store, question, llm):
    """Query the LLM using a retriever built from vectorstore."""
    retriever = vector_store.as_retriever(search_type="similarity", k=4)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    response = qa(question)
    return response

def search_arxiv(query, max_results=3):
    """Search Arxiv and return feedparser parsed results."""
    query = quote(query)
    base_url = "http://export.arxiv.org/api/query?"
    search_url = f"{base_url}search_query=all:{query}&start=0&max_results={max_results}"
    return feedparser.parse(search_url)

# -------------------- Main Script --------------------

if __name__ == "__main__":
    # Step 1: Search Arxiv
    query = "natural language processing"
    print(f"🔍 Searching Arxiv for: {query}")
    results = search_arxiv(query, max_results=3)

    # Step 2: Collect PDF URLs
    all_urls = []
    for entry in results.entries:
        pdf_url = next(link.href for link in entry.links if link.type == "application/pdf")
        all_urls.append(pdf_url)

    print("📄 PDF URLs:", all_urls)

    # Step 3: Connect to Pinecone
    index = connect_to_pinecone()

    # Step 4: Set up embeddings and chunks from the first paper
    embeddings, chunks = setup_embeddings_and_chunks(all_urls[0])

    # Step 5: Add chunks to Pinecone
    vector_store = add_to_vector_store(index, embeddings, chunks)

    # Step 6: Setup HuggingFace LLM
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        temperature=0.6,
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        max_new_tokens=512
    )

    # Step 7: Ask a question
    question = "What is the paper about?"
    print(f"🧠 Asking: {question}")
    response = query_llm(vector_store, question, llm)

    # Step 8: Display result
    print("\n🧠 Answer:\n", response["result"])
    print("\n🔍 Source Chunks:")
    for doc in response["source_documents"]:
        print("-", doc.page_content[:300].strip(), "\n")
