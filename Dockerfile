FROM python:3.9-slim

WORKDIR /app
RUN mkdir /app/logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY config.py .
COPY logging.conf .
COPY templates/ templates/

CMD ["python", "app.py"]
