# --- Stage 1: Builder ---
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# --- Stage 2: Final Image ---
FROM python:3.11-slim
WORKDIR /app
RUN useradd --create-home appuser
USER appuser
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*
COPY . .
EXPOSE 8000
CMD ["/home/appuser/.local/bin/gunicorn", "--workers", "3", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
