# Research Paper Chat Assistant

A web-based platform that lets users interact with research papers using state-of-the-art language models. Upload, search, and chat with papers — all in one seamless experience.

## Overview

This application enables users to:

1. **Upload and Ask:** Upload a research paper (PDF) and ask questions — get instant answers powered by an LLM.

2. **Persistent Chat Sessions:** Conversations with papers are stored and can be revisited later.

3. **Search and Interact:** Search papers via arXiv and interact with them on the fly without uploading.

4. **Topic-Aware Recommendations:** Uploaded and searched papers are classified into 17 predefined topics. The system recommends papers based on your dominant topic of interest.

## Techstack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask, Langchain
- **Database:** SQLite3
- **VectorDB:** FAISS
- **Models:** BERT, OpenAI GPT-4-nano
- **APIs:** arXiv, Google Scholar

Create a virtual environment and install dependencies: Install dependencies using `pip install -r requirements.txt`.

## Running the App

1. Clone the repository and navigate to the project directory.

2. Create a .env file in the project root and add the following variables:

- SECRET_KEY=your_flask_secret_key

- SQLALCHEMY_DATABASE_URI=sqlite:///database.db

- UPLOAD_FOLDER=path_to_folder_where_papers_are_stored

- OPENAI_API_KEY=your_openai_api_key
   
3. Run the Flask app: `flask run`

4. Open your browser and visit `http://localhost:5000`

## NLP Workflows

### RAG chat agent - 

![Scenario_ - visual selection (1)](https://github.com/user-attachments/assets/ffc9c638-6dc5-4dfd-93b4-bc94a11a423d)

### Reccommendation -

![Rec workflow](https://github.com/user-attachments/assets/864066be-7181-4f1b-8f11-7ff826aff134)

## Website workflow

![Scenario_ - visual selection](https://github.com/user-attachments/assets/b9935669-40b8-40ef-9908-3121c5da9915)


​

Group Members:

Mrunmayi Parker

Mohit Patel

Nahush Patil










