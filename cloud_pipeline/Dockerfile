FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Runs the pipeline on a schedule; override CMD with "python pipeline.py" for a one-off run
CMD ["python", "scheduler.py"]
