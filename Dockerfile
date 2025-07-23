FROM python:3.10

# Install required system dependencies
RUN apt-get update && apt-get install -y g++ cmake

# Set working directory
WORKDIR /app

# Copy all backend-infra files into container
COPY . .

# Build C++ shared library for word counting
RUN g++ -fPIC -shared -o libwordcount.so main.cpp

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2 requests

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
