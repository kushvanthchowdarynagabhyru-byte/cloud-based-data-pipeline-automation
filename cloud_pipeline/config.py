"""Central configuration. Values come from environment variables with safe defaults,
so the pipeline runs locally with zero setup and in the cloud with just env vars."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source: a local CSV path or an http(s) URL to a CSV file
SOURCE_URL = os.getenv("SOURCE_URL", os.path.join(BASE_DIR, "sample_data", "sales.csv"))

# Local folders / warehouse
STAGING_DIR = os.getenv("STAGING_DIR", os.path.join(BASE_DIR, "staging"))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "warehouse.db"))

# Cloud storage (optional). If S3_BUCKET is empty, the cloud upload step is skipped.
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_PREFIX = os.getenv("S3_PREFIX", "pipeline-output")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

# Scheduler
RUN_EVERY_MINUTES = int(os.getenv("RUN_EVERY_MINUTES", "60"))
