"""Pipeline orchestration: Extract -> Transform -> Load, with logging and retries."""
import logging
import time

import config
from extract import extract
from transform import transform
from load import load_to_warehouse, save_staging_file, upload_to_s3

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("pipeline")


def run_pipeline(retries: int = 3, delay_seconds: int = 5) -> bool:
    for attempt in range(1, retries + 1):
        try:
            log.info("=== Pipeline run started (attempt %d/%d) ===", attempt, retries)
            raw = extract(config.SOURCE_URL)
            clean = transform(raw)
            load_to_warehouse(clean, config.DB_PATH)
            staged = save_staging_file(clean, config.STAGING_DIR)
            upload_to_s3(staged, config.S3_BUCKET, config.S3_PREFIX, config.AWS_REGION)
            log.info("=== Pipeline run succeeded ===")
            return True
        except Exception:
            log.exception("Pipeline run failed")
            if attempt < retries:
                time.sleep(delay_seconds)
    log.error("Pipeline failed after %d attempts", retries)
    return False


if __name__ == "__main__":
    raise SystemExit(0 if run_pipeline() else 1)
