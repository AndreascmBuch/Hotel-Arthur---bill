# Base image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BIL_SERVICE=http://BIL_service:5000

# Set the working directory
WORKDIR /app

# Copy all files from the current directory to /app in the image
COPY . .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Execute this command when the container runs
CMD ["python", "app.py"]

