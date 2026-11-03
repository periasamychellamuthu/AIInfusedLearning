#set python on top of docker basic linux inorder to run python files
FROM python:3.13-slim

#Sets the working directory inside the container to /app
WORKDIR /app

COPY requirements.txt .
#Recursively run all the python packages
#--no-cache-dir  : Do not save the downloaded package cache on disk while installing.
#cache used to for the case of re-install packages
RUN pip install --no-cache-dir -r requirements.txt

#copy all the files in current folder only if run the docker in current folder
COPY . .

# 5. Train the model INSIDE the image (baked in at build time)
RUN python model_train.py

# 6. Declare which window use docker to get output
EXPOSE 8975

# 7. What runs the moment the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8975"]




