# Commands
# Construir: docker build --no-cache -t my_ocr_app .
# Executar:  docker run -p 8080:80 my_ocr_app
# === Build stage ===
FROM python:3.10-slim-buster as builder

# Install system packages
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

# Update pip and install ocrmypdf
RUN pip install --upgrade pip
RUN pip install ocrmypdf gunicorn

# === Application stage ===
FROM python:3.10-slim-buster as application

# Set the working directory to /app
WORKDIR /app

COPY --from=builder /usr/local /usr/local

# Copy the requirements file.
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./templates /app/templates
COPY . /app

# Create the uploads directory
RUN mkdir -p /app/uploads

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
CMD ["python", "app.py"]
