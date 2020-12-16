import os


if os.getenv("FLASK_ENV") == "development":
    from apps import demo
