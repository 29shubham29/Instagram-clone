#!/usr/bin/env python
import os
from app import celery, create_app
from config import Config

app = create_app(config_class=Config)
app.app_context().push()