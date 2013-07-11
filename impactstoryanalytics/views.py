import requests, os, json, logging, iso8601
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



@app.route('/active-users')
def active_users():
	active_users_keenio_query = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Viewed%20own%20profile&filters=%5B%7B%22property_name%22%3A%22days_since_account_created%22%2C%22operator%22%3A%22gte%22%2C%22property_value%22%3A1%7D%5D&timeframe=previous_24_hours&timezone=-25200&target_property=user.traits.email&interval=hourly"

	keenio_data = requests.get(active_users_keenio_query).json()["result"]
	timepoints = [datapoint["timeframe"]["start"] for datapoint in keenio_data]
	values = [datapoint["value"] for datapoint in keenio_data]

	date_format = "%a %I:%M%p"  # 'Wed 03:00PM'
	min_timepoint = iso8601.parse_date(timepoints[0])
	max_timepoint = iso8601.parse_date(timepoints[len(timepoints)-1])
	gecko_response = {
	    "item": values,
	    "settings": {
	     "axisx": [min_timepoint.strftime(date_format), max_timepoint.strftime(date_format)],
	     "axisy": [min(values), max(values)],
	     "colour": "ff9900"
	    }
	}

	resp = make_response(json.dumps(gecko_response, indent=4), 200)
	resp.mimetype = "application/json"
	return resp

