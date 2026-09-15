from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=70
)

mytext = """Text splitting and chunking is a fundamental technique in natural language processing 
and machine learning that involves breaking down large documents or texts into smaller, manageable 
pieces called chunks. This process is essential for several reasons: first, it allows language 
models and machine learning algorithms to process text within their token limits, as most large 
language models have maximum context windows that restrict the amount of text they can process 
at once. Second, chunking enables more efficient retrieval and processing of information, making 
it easier to search, index, and analyze large documents. The RecursiveCharacterTextSplitter is 
a sophisticated approach that recursively splits text based on different delimiters, starting 
with larger separators like paragraph breaks and gradually moving to smaller ones like sentences 
and individual words, ensuring that semantically related content stays together as much as 
possible. When configuring a text splitter, two critical parameters are chunk_size, which 
determines the maximum number of characters or tokens in each chunk, and chunk_overlap, which 
specifies how many characters from the end of one chunk should be repeated at the beginning of 
the next chunk, providing continuity and context preservation across chunks. Proper chunk sizing 
requires balancing competing objectives: chunks that are too small may lose important context 
and require many API calls for processing, while chunks that are too large may exceed model 
limitations and dilute the relevance of retrieved information. The overlap parameter is 
particularly important in retrieval-augmented generation systems, where chunks are used to 
retrieve relevant context for answering questions, as overlap ensures that important information 
spanning chunk boundaries won't be missed. Understanding text chunking is crucial for building 
effective applications with language models, whether for semantic search, question-answering 
systems, document summarization, or fine-tuning purposes, as the quality of chunking directly 
impacts the quality of downstream model outputs and the efficiency of the entire system."""

chunks = splitter.split_text(mytext)

print(len(chunks))

for chunk in chunks:
    print(chunk)
    print("---------------------------------")



