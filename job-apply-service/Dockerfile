# Use official Python image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

