# 🧠 Research Paper Chat Assistant

A web-based platform that lets users interact with research papers using state-of-the-art language models. Upload, search, and chat with papers — all in one seamless experience.

## 💡 Motivation

This project was born out of a real need:
While working on a research-heavy project, we found ourselves overwhelmed by the number of papers we had to go through. Understanding academic papers can be challenging, especially due to the technical language, domain-specific jargon, and complex structure.

Some key challenges we identified:

- Reading full papers is time-consuming, and not always necessary — sometimes, you just need specific insights.

- Papers outside one's area of expertise are particularly difficult to grasp quickly.

- Navigating through lengthy PDFs to find relevant sections can slow down productivity.

To solve this, we built an app that helps users interactively explore research papers. Instead of passively reading, users can upload a paper and ask questions, making the experience more efficient and intuitive.

For research enthusiasts, we added a search feature using arXiv and a recommendation engine that suggests papers based on the user’s most-read topics. This makes it easier to discover relevant research on the fly.

> Our goal was to create a one-stop solution for anyone who wants to simplify the process of reading, exploring, and learning from research papers — and we've developed an MVP to bring this vision to life.

🎯 Target Audience

- Students and professionals working on research projects

- Curious minds and paper enthusiasts

- Anyone looking to make sense of academic literature, faster



## 📌 Overview

This application enables users to:

1. **Upload and Ask:** Upload a research paper (PDF) and ask questions — get instant answers powered by an LLM.

2. **Persistent Chat Sessions:** Conversations with papers are stored and can be revisited later.

3. **Search and Interact:** Search papers via arXiv and interact with them on the fly without uploading.

4. **Topic-Aware Recommendations:** Uploaded and searched papers are classified into 17 predefined topics. The system recommends papers based on your dominant topic of interest.

## 🧰 Techstack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask, Langchain
- **Database:** SQLite3
- **VectorDB:** FAISS
- **Models:** BERT, OpenAI GPT-4-nano
- **APIs:** arXiv, Google Scholar

Create a virtual environment and install dependencies: Install dependencies using `pip install -r requirements.txt`.

## 🚀 Running the App

1. Clone the repository and navigate to the project directory.

2. Create a .env file in the project root and add the following variables:

- SECRET_KEY=your_flask_secret_key

- SQLALCHEMY_DATABASE_URI=sqlite:///database.db

- UPLOAD_FOLDER=path_to_folder_where_papers_are_stored

- OPENAI_API_KEY=your_openai_api_key
   
3. Run the Flask app: `flask run`

4. Open your browser and visit `http://localhost:5000`

## ⚙️ NLP Workflows

### RAG chat agent - 

![Scenario_ - visual selection (1)](https://github.com/user-attachments/assets/ffc9c638-6dc5-4dfd-93b4-bc94a11a423d)

### Topic Classification & Reccommendation -

![Scenario_ - visual selection (1)](https://github.com/user-attachments/assets/3e98c744-451e-4ba7-afa7-729a6ea78d29)


## Website workflow

![Scenario_ - visual selection](https://github.com/user-attachments/assets/b9935669-40b8-40ef-9908-3121c5da9915)


​

Group Members:

Mrunmayi Parker

Mohit Patel

Nahush Patil










