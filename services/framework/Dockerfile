FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY soc2.py iso27001.py mappings.py ./

CMD ["python", "soc2.py"] 