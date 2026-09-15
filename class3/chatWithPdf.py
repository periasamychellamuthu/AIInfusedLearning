import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from models import getHuggingFaceEmdedderModelName, getGroqLangChainModel, getGroqParser

from langchain_core.prompts import ChatPromptTemplate

import gradio as gr

state = {"db": None} 

def build_index(pdf_path):
    pages = PyPDFLoader(pdf_path).load();
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    embedder = HuggingFaceEmbeddings(model_name=getHuggingFaceEmdedderModelName())
    db = Chroma.from_documents(chunks, embedder)
    return db

model = getGroqLangChainModel()
parser = getGroqParser()

prompt = ChatPromptTemplate.from_template("""
You are a helpful PDF assistant. Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I couldn't find that in the document."
After your answer, list the page numbers you used as: Sources: page X, page Y.

Context:
{context}

Question: {question}
""")

def ask(db, question):
    chunks  = db.similarity_search(question, k=4)
    context = "\n\n".join(
        f"[page {c.metadata['page']+1}] {c.page_content}" for c in chunks)
    chain = prompt | model | parser
    return chain.invoke({"context": context, "question": question})

def upload(pdf):
    state["db"] = build_index(pdf.name)
    return "✅ PDF indexed! Ask me anything about it."

def chat(message, history):
    if state["db"] is None:
        return "Please upload a PDF first 📄"
    return ask(state["db"], message)

with gr.Blocks(title="📄 Chat with your PDF") as demo:
    gr.Markdown("## 📄 Chat with your PDF (powered by RAG)")
    pdf    = gr.File(label="Upload a PDF", file_types=[".pdf"])
    status = gr.Markdown()
    pdf.upload(upload, inputs=pdf, outputs=status)
    gr.ChatInterface(fn=chat)

demo.launch()