#set python on top of docker basic linux inorder to run python files
FROM python:3.12-slim

#Sets the working directory inside the container to /app
WORKDIR /app

COPY requirements.txt .
#Recursively run all the python packages
#--no-cache-dir  : Do not save the downloaded package cache on disk while installing.
#cache used to for the case of re-install packages
#RUN --mount=type=cache,target=/root/.cache/pip pip install --default-timeout=120 --retries 5 -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Pre-download the embedding model at build time (requires internet during build)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# These only affect huggingface_hub / transformers behavior — not Docker itself
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1

#copy all the files in current folder only if run the docker in current folder
COPY . .

# Declare which window use docker to get output
EXPOSE 8000

# What runs the moment the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]




