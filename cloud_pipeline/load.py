"""LOAD: write to a SQL warehouse (SQLite here) and optionally upload to AWS S3."""
import logging
import os
import sqlite3
from datetime import datetime, timezone

import pandas as pd

log = logging.getLogger(__name__)


def load_to_warehouse(df: pd.DataFrame, db_path: str, table: str = "sales") -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
        # Small aggregate table, handy for dashboards
        summary = (
            df.groupby("order_month", as_index=False)
            .agg(orders=("order_id", "count"), revenue=("total_amount", "sum"))
            .round(2)
        )
        summary.to_sql("monthly_summary", conn, if_exists="replace", index=False)
    log.info("Loaded %d rows into %s (table '%s')", len(df), db_path, table)


def save_staging_file(df: pd.DataFrame, staging_dir: str) -> str:
    os.makedirs(staging_dir, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(staging_dir, f"sales_clean_{stamp}.csv")
    df.to_csv(path, index=False)
    log.info("Saved cleaned file to %s", path)
    return path


def upload_to_s3(file_path: str, bucket: str, prefix: str, region: str) -> None:
    if not bucket:
        log.info("S3_BUCKET not set - skipping cloud upload")
        return
    import boto3  # imported lazily so local runs don't need AWS

    key = f"{prefix}/{os.path.basename(file_path)}"
    boto3.client("s3", region_name=region).upload_file(file_path, bucket, key)
    log.info("Uploaded to s3://%s/%s", bucket, key)
