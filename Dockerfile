# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
