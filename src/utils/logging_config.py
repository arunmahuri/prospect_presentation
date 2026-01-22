# logging_config.py
from datetime import datetime
import sys
from pathlib import Path
from loguru import logger
from src.utils.config import LoggingConfig

log_cfg = LoggingConfig()

def setup_logging():
    logger.remove()

    log_dir = Path(log_cfg.LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_app.log"

    # Console
    logger.add(
        sys.stdout,
        level=log_cfg.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        enqueue=True,
    )

    # File
    logger.add(
        log_file,
        level=log_cfg.LOG_LEVEL,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        enqueue=True,
    )

    logger.info(f"Logging initialized at level {log_cfg.LOG_LEVEL}")
    return logger