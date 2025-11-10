# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

SHELL [ "/bin/bash", "-c" ]

ENV SHELL=/bin/bash

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ENV NVM_DIR=/root/.nvm

RUN apt-get update
RUN apt-get install -y curl

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt install -y nodejs

ENV NODE_PATH=$NVM_DIR/v20/lib/node_modules
ENV PATH=$NVM_DIR/v20/bin:$PATH
ADD . /app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


#EXPOSE the port, for now default is 8080 cause it's the only one really allowed by HuggingFace
EXPOSE 8000

# Run run.py when the container launches
CMD ["bash", "-c" ,"uvicorn src.main:app --host 0.0.0.0"]