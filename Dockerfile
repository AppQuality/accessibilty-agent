# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster
# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ENV NVM_DIR=/root/.nvm

RUN apt update
RUN apt install -y curl

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash \
&& . /root/.nvm/nvm.sh \
&& nvm install 20 \
&& nvm alias default 20 \
&& nvm use default

ENV NODE_PATH=$NVM_DIR/v20/lib/node_modules
ENV PATH=$NVM_DIR/v20/bin:$PATH
ADD . /app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


#EXPOSE the port, for now default is 8080 cause it's the only one really allowed by HuggingFace
EXPOSE 8000

# Run run.py when the container launches
CMD ["uvicorn","src.main:app", "--host", "0.0.0.0"]