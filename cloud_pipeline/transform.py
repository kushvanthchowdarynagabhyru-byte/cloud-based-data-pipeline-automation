"""TRANSFORM: clean, validate and enrich the raw data."""
import logging
import pandas as pd

log = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"order_id", "order_date", "customer", "product", "quantity", "unit_price"}


def transform(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    before = len(df)
    df = df.copy()

    # Standardise text
    df["customer"] = df["customer"].astype(str).str.strip().str.title()
    df["product"] = df["product"].astype(str).str.strip().str.title()

    # Type conversion (bad values become NaN/NaT and are dropped below)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Data quality rules
    df = df.drop_duplicates(subset="order_id")
    df = df.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    # Enrichment
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df["processed_at"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M:%S")

    log.info("Transform kept %d of %d rows (%d rejected)", len(df), before, before - len(df))
    return df.reset_index(drop=True)
