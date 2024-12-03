FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    libstdc++6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

