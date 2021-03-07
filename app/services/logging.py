import google.cloud.logging
import app.config.app as app_config
import logging

level = logging.INFO


def setup_logging():
    if app_config.is_prod:
        client = google.cloud.logging.Client()
        client.get_default_handler()
        client.setup_logging(log_level=level)
    else:
        logging.root.setLevel(level=level)
