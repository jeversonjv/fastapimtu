# Use the official Python base image with the desired version
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose the port that the FastAPI app will listen on
EXPOSE 8000
