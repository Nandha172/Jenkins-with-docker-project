# Use official Python image as base
FROM python:3.9  

# Set working directory inside the container
WORKDIR /app  

# Copy all files from your project directory into the container
COPY . .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Expose port 5000 for Flask
EXPOSE 5000  

# Command to run the Flask app
CMD ["python", "app.py"]

