def getEmbedderModelName():
    return "all-MiniLM-L6-v2"

def getEmbedder():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=getEmbedderModelName())
