from celery import Celery, platforms
from api.authentication.model import User
from utils.ext import db
from api import create_app
from os import environ
import logging

config_name = 'config.settings.{0}'.format(environ.get("FLASK_CONFIG", 'Devops'))
flask_app = create_app(config_name)

app = Celery('devops')
app.config_from_object(config_name)

platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def maintain_monitor_active(self, item_id=None):
    try:
        with flask_app.app_context():
            pass

    except Exception as e:
        if self.request.retries <= 2:
            logging.error("error: %s...retry %s " % (e, self.request.retries))
            raise self.retry(exc=e, countdown=5, max_retries=3)


if __name__ == '__main__':
    app.start()
