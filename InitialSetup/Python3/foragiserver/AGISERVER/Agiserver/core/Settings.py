import os
from pathlib import Path


debug = True

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')
CONFIG_DIR = os.path.join(BASE_DIR, 'core/config/config.ini')
BASE_LOG_FILE = 'ivrs_basic_log.log'
API_LOG_TABLE = 'ivrs_basic_log'

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

