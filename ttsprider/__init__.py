#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create_app(config):
    # init Flask application object
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(config)

    # init flask-login
    from ttsprider.core.login import login_manager
    login_manager.init_app(app)

    # init redis
    from ttsprider.core.db import stationNameInit
    stationNameInit()

    from flask_bootstrap import Bootstrap
    Bootstrap(app)

    from ttsprider.celerys import celery
    celery = celery.init_celery(app)

    import controlers
    controlers.Register_Blueprints(app)
    
    return app
