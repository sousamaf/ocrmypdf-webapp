# How to build: 
# docker build --no-cache -t my_ocr_app .

# How to run:
# docker run -p 8080:80 my_ocr_app

# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \ 
    tesseract-ocr-por \
    qpdf \
    ghostscript \
    unpaper \
    libcairo2 \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Update pip 
RUN pip install --upgrade pip
# Install ocrmypdf
RUN pip install ocrmypdf

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD ./templates /app/templates
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

