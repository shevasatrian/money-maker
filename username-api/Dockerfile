FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY api/requirements.txt ./api/requirements.txt
RUN pip install -r api/requirements.txt

COPY api ./api

EXPOSE 8000

# Render injects $PORT; default to 8000 locally.
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
