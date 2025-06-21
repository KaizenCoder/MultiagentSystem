FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

CMD ["uvicorn", "taskmaster_pool_supervisor:app", "--host", "0.0.0.0", "--port", "8001"]
