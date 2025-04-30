# from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models.paper import Paper
from app import db
import os
from rag.connect_memory_with_llm import query_llm
from app.models.conversation import Conversation
from app.models.conversation_session import ConversationSession
from flask import Blueprint, request, jsonify, render_template


import traceback

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/ask", methods=['POST'])
@login_required
def ask_question():
    data = request.get_json()
    paper_id = data.get('paper_id')
    question = data.get("question")
    session_id = data.get('session_id')


    paper = Paper.query.filter_by(id=paper_id, user_id=current_user.id).first()
    if not paper:
        return jsonify({"message": "Paper not found"}), 404

    paper_base = paper.filename.rsplit(".", 1)[0]
    vectorstore_path = os.path.join("vectordb", paper_base)

    # 🧪 Instead of calling real LLM, generate dummy answer
    dummy_answer = f"This is a dummy answer for your question: '{question}'"
    dummy_sources = ["source1.pdf", "source2.pdf"]

    # Save to Conversation table
    convo = Conversation(
        question=question,
        answer=dummy_answer,
        user_id=current_user.id,
        paper_id=paper.id,
        session_id=session_id
    )
    db.session.add(convo)
    db.session.commit()

    # Return dummy answer
    return jsonify({
        "answer": dummy_answer,
        "sources": dummy_sources
    }), 200

#@chat_bp.route("/ask", methods=["POST"])
#@login_required

# def ask_question():
#     try:
#         data = request.get_json()
#         paper_id = data.get('paper_id')
#         question = data.get("question")
#         session_id = data.get("session_id")

#         if not paper_id or not question or not session_id:
#             return jsonify({"message": "Missing paper_id, question, or session_id"}), 400

#         paper = Paper.query.filter_by(id=paper_id, user_id=current_user.id).first()
#         if not paper:
#             return jsonify({"message": "Paper not found"}), 404

#         vectorstore_path = os.path.join("vectordb", paper.hash)
#         response = query_llm(question, vectorstore_path)
#         answer = response['answer']

#         convo = Conversation(
#             question=question,
#             answer=answer,
#             user_id=current_user.id,
#             paper_id=paper.id,
#             session_id=session_id
#         )

#         db.session.add(convo)
#         db.session.commit()

#         return jsonify({
#             "answer": response["answer"],
#             "sources": response["sources"]
#         }), 200

#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"message": "Internal server error", "error": str(e)}), 500


@chat_bp.route("/history", methods=["GET"])
@login_required
def get_history():
    paper_id = request.args.get("paper_id")  # optional
    session_id = request.args.get("session_id")


    if not session_id:
        return jsonify({"message": "Missing session_id"}), 400

    query = Conversation.query.filter_by(user_id=current_user.id)  # FIXED HERE

    query = query.filter_by(session_id=session_id)
    if paper_id:
        query = query.filter_by(paper_id=paper_id)


    history = query.order_by(Conversation.timestamp.asc()).all()  # optional: use asc() if you want chronological

    return jsonify([
        {
            "id": c.qid,
            "question": c.question,
            "answer": c.answer,
            "timestamp": c.timestamp.isoformat(),
            "paper_id": c.paper_id,
            "session_id": c.session_id
        }
        for c in history
    ])

@chat_bp.route("/session", methods=["POST"])
@login_required
def create_session():
    print("[SERVER LOG] /session endpoint triggered") 
    data = request.get_json()

    # Optional: allow frontend to send session name, else default to "New Chat"
    session_name = data.get("session_name", "New Chat")
    print("Session name - ", session_name)

    new_session = ConversationSession(
        session_name=session_name,
        user_id=current_user.id
    )

    db.session.add(new_session)
    db.session.commit()

    print(f"[SERVER LOG] created New Session: {new_session.session_id}, Name: {session_name}")
    return jsonify({
        "message": "Session created successfully",
        "session_id": new_session.session_id,
        "session_name": new_session.session_name
    }), 201

@chat_bp.route("/", methods=["GET"])
@login_required
def chat_ui():
    return render_template("chat.html")

@chat_bp.route("/session_list", methods=["GET"])
@login_required
def get_session_list():
    sessions = ConversationSession.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            "session_id": s.session_id,
            "session_name": s.session_name
        }
        for s in sessions
    ])

