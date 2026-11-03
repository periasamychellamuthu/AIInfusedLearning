from utility.config import REPO_ROOT

# absolute path, so the same db is used no matter which folder the script is run from
CHROMA_DIR = str(REPO_ROOT / "chroma_db")

def getChromaDB(embedder):
    from langchain_chroma import Chroma
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embedder)
