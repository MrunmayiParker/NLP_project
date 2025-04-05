from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


import streamlit as st
from dotenv import load_dotenv
import os

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


# template

prompt =  ChatPromptTemplate.from_messages(
    [
        ("system", "You are helping to assist to understand and analyse the research papers"),
        ("user", "Question : {question}")
    ]
)

# streamlit

st.title('Langchain Demo With OPENAI API')
input_text=st.text_input("Search the topic u want")


# open ai

llm = ChatOpenAI(model = "gpt-4.0")
ouptut_parser = StrOutputParser()
chain = prompt|llm|ouptut_parser

if input_text:
    st, write(chain.invoke({'question': input_text}))

    