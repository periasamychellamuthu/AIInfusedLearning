import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from models import getHuggingFaceEmdedderModelName
from chroma import getChromaPersistenceDirectoryPath

docs = [
    "Our return policy allows refunds within 30 days of purchase.",
    "Shipping is free for orders above ₹999 across India.",
    "For corporate orders above 50 units, contact sales@example.com.",
    "Our office is in Indiranagar, Bangalore. Open Mon-Fri 10am-7pm.",
]

splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10);
chunks = splitter.create_documents(docs);

embedder = HuggingFaceEmbeddings(model_name=getHuggingFaceEmdedderModelName())

db =Chroma.from_documents(chunks, embedder, persist_directory=getChromaPersistenceDirectoryPath())

print(f"Indexed {len(chunks)} chunks 🎉")