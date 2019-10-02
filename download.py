from flask import current_app,render_template
from app import celery

@celery.task
def download(image):
    pass