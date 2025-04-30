# app/routes/search_chat.py

from flask import Blueprint, request, jsonify, render_template
from app.routes.search import load_vector_store  # ✅ import here, reuse it
from dotenv import load_dotenv
import os
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceEndpoint

load_dotenv()

search_ui_bp = Blueprint('search_ui', __name__, url_prefix='/search')

@search_ui_bp.route('/chat', methods=['GET'])
def search_chat_page():
    return render_template('search_chat.html')

@search_ui_bp.route('/ask', methods=['POST'])
def search_ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"message": "Missing question"}), 400

    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        temperature=0.6,
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        max_new_tokens=512
    )

    vector_store = load_vector_store()  # ✅ reused from search.py
    retriever = vector_store.as_retriever(search_type="similarity", k=4)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    response = qa(question)

    return jsonify({
        "answer": response["result"],
        "sources": [doc.metadata for doc in response["source_documents"]]
    }), 200
