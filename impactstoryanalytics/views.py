import requests, os, json, logging
from impactstoryanalytics import app

from flask import request, abort, make_response, g, redirect, url_for
from flask import render_template

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import func


logger = logging.getLogger("impactstoryanalytics.views")


# static pages
@app.route('/')
def index():
    return render_template('index.html')
