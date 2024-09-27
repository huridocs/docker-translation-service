import logging
import os
from pathlib import Path

import graypy

SRC_PATH = Path(__file__).parent.absolute()
ROOT_PATH = Path(__file__).parent.parent.absolute()
TRANSLATIONS_PORT = 11434
LANGUAGES_SHORT = ["en", "fr", "es", "ru", "ar", "sp"]
LANGUAGES = ["English", "French", "Spanish", "Russian", "Arabic", "Spanish"]

QUEUES_NAMES = os.environ.get("QUEUES_NAMES", "translations development_translations")

GRAYLOG_IP = os.environ.get("GRAYLOG_IP")
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
MODEL = os.environ.get("MODEL", "aya:35b")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

handlers = [logging.StreamHandler()]

if GRAYLOG_IP:
    handlers.append(graypy.GELFUDPHandler(GRAYLOG_IP, 12201, localname="pdf_metadata_extraction"))

logging.root.handlers = []
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)
service_logger = logging.getLogger(__name__)

if LOGGING_LEVEL == "WARNING":
    service_logger.setLevel(logging.WARNING)
else:
    service_logger.setLevel(logging.INFO)
