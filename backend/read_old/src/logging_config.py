import logging
import logging.handlers
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Formatter
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# App log
app_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, 'app.log'), maxBytes=2*1024*1024, backupCount=5, encoding='utf-8')
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# Error log
error_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, 'error.log'), maxBytes=2*1024*1024, backupCount=5, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Access log (يمكن ربطه مع uvicorn لاحقًا)
access_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, 'access.log'), maxBytes=2*1024*1024, backupCount=5, encoding='utf-8')
access_handler.setLevel(logging.INFO)
access_handler.setFormatter(formatter)

# الجذر
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(app_handler)
root_logger.addHandler(error_handler)

# لوجر الوصول (يمكن ربطه مع uvicorn)
access_logger = logging.getLogger('access')
access_logger.setLevel(logging.INFO)
access_logger.addHandler(access_handler) 