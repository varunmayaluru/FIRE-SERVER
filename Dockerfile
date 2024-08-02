# Use the official Python image from the Docker Hub
FROM python:3.10-slim-buster

# Create dir within the container to house app code
RUN mkdir /usr/src/app

# Copy app code from current dir in to app code dir
COPY . /usr/src/app

# Set the working dir to the app code dir
WORKDIR /usr/src/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
