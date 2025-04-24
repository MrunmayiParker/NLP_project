from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.paper import Paper
from rag.create_memory_llm import create_vector_store
import hashlib
from datetime import datetime, timezone


upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compute_file_hash(file):
    file.seek(0)
    content = file.read()
    file.seek(0)  # Reset file pointer for saving
    return hashlib.sha256(content).hexdigest()

@upload_bp.route("/paper", methods=["POST"])
@login_required
def upload_paper():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    file_hash = compute_file_hash(file)

    existing = Paper.query.filter_by(hash=file_hash).first()
    if existing:
        return jsonify({
            "message": "Paper already exists",
            "paper_id": existing.id
        }), 200
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        paper_id = filename.rsplit('.', 1)[0]
        vectorstore_path = os.path.join("vectordb", paper_id)
        if not os.path.exists(vectorstore_path):
            create_vector_store(filepath, vectorstore_path)

        paper = Paper(filename=filename, filepath=filepath, upload_date=datetime.now(timezone.utc),user_id=current_user.id, hash=file_hash)
        db.session.add(paper)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully", "paper_id": paper.id}), 201

    return jsonify({"message": "Invalid file type"}), 400
