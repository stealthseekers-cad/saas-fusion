FROM python:3.11-slim
# Create app directory & user
RUN useradd -m appuser
WORKDIR /home/appuser/app
# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt &&     pip install gunicorn
# Copy source and set ownership
COPY . .
RUN chown -R appuser:appuser /home/appuser/app
# Switch to non-root for runtime safety
USER appuser
# Gunicorn is now in PATH and we bind to the PORT variable provided by Cloud Run
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080"]
