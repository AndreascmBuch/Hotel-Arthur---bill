# Base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt ./

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files from the current directory to /app in the image
COPY . .

# Run database setup script
RUN python database_bil.py

EXPOSE 5001

# Execute this command when the container runs
CMD ["python", "app.py"]

