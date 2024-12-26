# Use the official Python base image
FROM python:3.x-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the default command to run your script
ENTRYPOINT ["python", "./script.py"]