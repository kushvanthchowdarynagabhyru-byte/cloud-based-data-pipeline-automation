"""EXTRACT: read raw data from a local file or a remote URL (cloud/API/S3 pre-signed link)."""
import logging
import pandas as pd

log = logging.getLogger(__name__)


def extract(source: str) -> pd.DataFrame:
    log.info("Extracting data from %s", source)
    df = pd.read_csv(source)  # works for local paths and http(s) URLs
    log.info("Extracted %d rows, %d columns", *df.shape)
    return df
