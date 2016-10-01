#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Blueprint


tt_error = Blueprint('tt_error', __name__, template_folder="../templates/error")

@tt_error.app_errorhandler(404)
def page_not_found(error):
     return render_template('404.html')


@tt_error.app_errorhandler(500)
def server_error(error):
    return render_template('500.html')
