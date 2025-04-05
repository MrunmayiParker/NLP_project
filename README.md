NLP-Powered Research Paper Explorer
Problem Statement

1. Introduction
With the rapid growth of academic research, finding relevant papers and extracting useful insights has become increasingly challenging. Researchers often struggle to navigate through massive volumes of literature, hindering the pace of innovation and discovery.
This project aims to develop an NLP-powered Research Paper Explorer that streamlines the discovery, exploration, and analysis of academic literature. Our system leverages advanced natural language processing techniques including Retrieval-Augmented Generation (RAG), semantic search, and similarity-based recommendation models to make the research process smarter and more efficient.

Objectives
Build a RAG-based chatbot that can answer research-related queries using retrieved excerpts from relevant papers.
Develop a semantic search engine that allows users to find research papers using natural language queries.
Implement a similarity-based paper recommendation system to suggest related research based on user input or selected documents.
Create a user-friendly interface for interactive exploration, filtering, and reading of research literature.

Features
3.1 RAG-Based Chatbot for Q&A
Utilizes Retrieval-Augmented Generation to answer user queries with contextually accurate information drawn from relevant papers.
Supports natural language question answering for enhanced user experience.
Uses vector embeddings for efficient and accurate document retrieval.

3.2 Semantic Search Engine
Empowers users to search using natural language instead of relying on strict keyword-based queries.
Employs Transformer-based models (e.g., BERT, SBERT, or T5) to compute semantic similarity scores between queries and paper abstracts.
Supports advanced filtering options such as publication year, authors, and research domain.

3.3 Find Similar Papers
Given a paper or abstract, recommends similar papers using cosine similarity of document embeddings.
Leverages pre-trained NLP models to compute contextual similarity between research texts.
Aids in literature discovery by surfacing relevant papers users may have missed.

Suggested Workflow:
1. Input paper or abstract
  
2. Text processing:
     -lowercasing
     -Removing special characters, extra whitespaces, etc
     -Removing stopwords
     -Tokenization
   
3. Embedding Generation
  -Use a pre-trained NLP model to convert text to a dense vector (embedding):
    Popular choices: Sentence-BERT, SciBERT, Universal Sentence Encoder, etc.
    These models map semantically similar texts to nearby points in vector space.
   
4. Retrieve Stored Embeddings
  -Load a precomputed embedding database:
    Each paper in the dataset has its abstract/title embedded and stored.
    Stored using tools like FAISS, Annoy, or simply in a NumPy array or database for fast access.
   
5. Cosine Similarity Computation
For each paper in the database:
Compute cosine similarity between its embedding and the query embedding.

6. Rank and Filter Results
  -Sort the papers by similarity score (descending order).
  -Return the top N most similar papers.
  -Filter results based on publication date, domain, etc.
  -Add a minimum threshold for similarity.
​

LLM Chatbot Research
As part of the RAG chatbot development, we researched and tested multiple open-source and API-based large language models (LLMs) for performance, cost, and flexibility.

Findings:
Google AI Studio (Gemini models): Offers models with strong reasoning capabilities and easy integration.
Mistral AI: Lightweight and efficient models ideal for budget-conscious deployments without sacrificing too much on performance.
Other open LLMs such as LLaMA, OpenChat, and Falcon were also considered for local deployment options. 
These LLMs were tested with research-related queries, and both Google AI Studio and Mistral AI provided consistently high-quality responses with minimal setup overhead, making them suitable candidates for the final integration.

Group Members:
Mrunmayi Parker
Mohit Patel
Nahush Patil










