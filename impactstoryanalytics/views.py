import requests, os, json, logging
from impactstoryanalytics import app, gmail

from flask import request, abort, make_response, g, redirect, url_for
from flask import render_template

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import func


logger = logging.getLogger("impactstoryanalytics.views")


# static pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inbox-count')
def inbox_count():
    count = gmail.count_threads_in_inbox(
        os.getenv("GMAIL_CLIENT_ID"),
        os.getenv("GMAIL_CLIENT_SECRET"),
        os.getenv("GMAIL_REFRESH_TOKEN_HEATHER"),
        os.getenv("GMAIL_ADDRESS_HEATHER")
    )

    return make_response(str(count))
