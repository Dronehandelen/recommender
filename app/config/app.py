import os

is_prod = os.getenv('ENV_NAME') == "production"
sentry_url = os.getenv("SENTRY_URL")
