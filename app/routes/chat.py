from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models.paper import Paper
from app import db
import os
from rag.connect_memory_with_llm import query_llm
from app.models.conversation import Conversation

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/ask", methods=['POST'])
@login_required
def ask_question():
    data = request.get_json()
    paper_id = data.get('paper_id')
    question = data.get("question")

    paper = Paper.query.filter_by(id=paper_id, user_id=current_user.id).first()
    if not paper:
        return jsonify({"message": "Paper not found"}), 404

    paper_base = paper.filename.rsplit(".", 1)[0]
    vectorstore_path = os.path.join("vectordb", paper_base)

    response = query_llm(question, vectorstore_path)
    answer = response['answer']

    convo = Conversation(question=question, answer=answer, userid=current_user.id, paperid=paper.id)

    db.session.add(convo)
    db.session.commit()

    return jsonify({
        "answer": response["answer"],
        "sources": response["sources"]
    })

@chat_bp.route("/history", methods=["GET"])
@login_required
def get_history():
    paper_id = request.args.get("paper_id")  # optional

    query = Conversation.query.filter_by(userid=current_user.id)
    if paper_id:
        query = query.filter_by(paperid=paper_id)

    history = query.order_by(Conversation.timestamp.desc()).all()

    return jsonify([
        {
            "id": c.id,
            "question": c.question,
            "answer": c.answer,
            "timestamp": c.timestamp.isoformat(),
            "paper_id": c.paperid
        }
        for c in history
    ])

