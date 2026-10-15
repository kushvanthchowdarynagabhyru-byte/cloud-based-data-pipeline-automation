# Cloud-Based Data Pipeline Automation

A simple ETL pipeline: **Extract** a CSV (local file or URL) -> **Transform** (clean, validate, enrich) -> **Load** into a SQLite warehouse and, optionally, AWS S3. A scheduler runs it automatically and a Dockerfile makes it deployable to any cloud.

## Run locally
    pip install -r requirements.txt
    python pipeline.py        # one-off run
    python scheduler.py       # repeat every RUN_EVERY_MINUTES (default 60)

## Configuration (environment variables)
| Variable | Default | Purpose |
|---|---|---|
| SOURCE_URL | sample_data/sales.csv | CSV path or http(s) URL |
| DB_PATH | warehouse.db | SQLite warehouse file |
| STAGING_DIR | staging | Cleaned CSV output |
| S3_BUCKET | (empty) | Set to enable S3 upload |
| S3_PREFIX | pipeline-output | Key prefix in the bucket |
| AWS_REGION | ap-south-1 | AWS region |
| RUN_EVERY_MINUTES | 60 | Scheduler interval |

## Docker / cloud
    docker build -t data-pipeline .
    docker run -e S3_BUCKET=my-bucket -e RUN_EVERY_MINUTES=30 data-pipeline

On AWS, run the container on ECS/Fargate or EC2 with an IAM role that allows `s3:PutObject`.
