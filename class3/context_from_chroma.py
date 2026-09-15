import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from models import getHuggingFaceEmdedderModelName, getGroqLangChainModel, getGroqParser, getCrossEncoderModel
from chroma import getChromaPersistenceDirectoryPath
from sentence_transformers import CrossEncoder

embedder = HuggingFaceEmbeddings(model=getHuggingFaceEmdedderModelName())
reranker = CrossEncoder(getCrossEncoderModel())
db = Chroma(persist_directory=getChromaPersistenceDirectoryPath(), embedding_function=embedder)

model= getGroqLangChainModel()
parser = getGroqParser()

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below. If the context doesn't contain
the answer, say "I don't know." Be concise and quote facts directly.

Context:
{context}

Question: {question}
""")

def return_with_rerank(question, top_k=3):
    chunks = db.similarity_search(question, k=25)    #Bi-encoding - grab 25 cheap candidates
    pairs = [(question, c.page_content) for c in chunks]
    scores = reranker.predict(pairs)

    return [c for _, c in sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)[:top_k]]


def rag_answer(question):
    chunks = return_with_rerank(question, 3)
    context = "\n\n".join(c.page_content for c in chunks)
    chain = prompt | model | parser

    return chain.invoke({"context": context, "question": question})

print(rag_answer("How long do I have to return something?"))
