FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth.py format.py git.py ./

CMD ["python", "auth.py"]  # Replace with the actual entry point