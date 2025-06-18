# --- Étape 1: Builder ---
FROM python:3.11-slim as builder
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY orchestrator/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Étape 2: Final ---
FROM python:3.11-slim AS final

# Create a non-root user
WORKDIR /home/appuser/app
RUN groupadd -r appuser && useradd --no-create-home -r -g appuser appuser

# Copy installed wheels from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copy application code
COPY . /home/appuser/app/
RUN chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

ENV PYTHONPATH=/home/appuser/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8002

# CORRECTIF: Réduction du nombre de threads de 8 à 4 pour optimiser la RAM avec GPT/Claude (I/O bound)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--threads", "4", "--graceful-timeout", "60", "app.main:app", "--bind", "0.0.0.0:8002"] 