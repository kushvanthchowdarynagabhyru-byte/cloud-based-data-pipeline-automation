"""Automation: runs the pipeline on a fixed interval (run this as the container's main process)."""
import time

import schedule

import config
from pipeline import run_pipeline, log

if __name__ == "__main__":
    log.info("Scheduler started: running every %d minute(s)", config.RUN_EVERY_MINUTES)
    run_pipeline()  # run once immediately
    schedule.every(config.RUN_EVERY_MINUTES).minutes.do(run_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(1)
