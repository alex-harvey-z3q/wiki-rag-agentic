FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
COPY indexer ./indexer
RUN pip install --no-cache-dir .
CMD ["python", "-m", "indexer.main"]
