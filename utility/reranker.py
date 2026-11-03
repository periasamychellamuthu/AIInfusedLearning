def getCrossEncoderModelName():
    return "cross-encoder/ms-marco-MiniLM-L6-v2"

def getReranker():
    from sentence_transformers import CrossEncoder
    return CrossEncoder(getCrossEncoderModelName())
