# Sample Dockerfile for apt-scraper
FROM python:3.11.7-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "src/main.py"]

# TODO: Enhance Dockerfile for production use.
