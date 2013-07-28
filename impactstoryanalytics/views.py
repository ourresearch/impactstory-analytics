import os
import sys
import json
import logging
import hashlib
import analytics
from impactstoryanalytics import app
from impactstoryanalytics import widgets
from impactstoryanalytics.widgets import papertrail_alerts
from impactstoryanalytics.widgets import api_key_item_creates
from impactstoryanalytics.widgets import api_key_item_views
from impactstoryanalytics.widgets import hourly_uniques
from impactstoryanalytics.widgets import products_per_profile
from impactstoryanalytics.widgets import signup_growth
from impactstoryanalytics.widgets import signup_funnel
from impactstoryanalytics.widgets import monthly_active_users
from impactstoryanalytics.widgets import daily_new_users
from impactstoryanalytics.widgets import daily_api_calls
from impactstoryanalytics.widgets import rescuetime
from impactstoryanalytics.widgets import gmail
from impactstoryanalytics.widgets import github
from impactstoryanalytics.widgets import latestprofile
from impactstoryanalytics.widgets import itemsbycreateddate
from impactstoryanalytics.widgets import uservoice_tickets
from impactstoryanalytics.widgets import embedded_widget_use
from impactstoryanalytics.widgets import uservoice_suggestions
from impactstoryanalytics.widgets import javascript_errors
from impactstoryanalytics.widgets import profiles_per_genre
from impactstoryanalytics.widgets import api_keys_minted
from impactstoryanalytics.widgets import importers_used
from impactstoryanalytics.widgets import provider_requests
from impactstoryanalytics.widgets import profile_load_times

from impactstoryanalytics.widgets.widget import Widget

from flask import request, abort, make_response, g, redirect, url_for
from flask import render_template
from flask.ext.assets import Environment, Bundle

logger = logging.getLogger("impactstoryanalytics.views")

# define dashboards
dashboards = {
    "engagement": [
        signup_growth.Signup_growth(),
        signup_funnel.Signup_funnel(),
        monthly_active_users.Monthly_active_users()
    ],
    "productivity": [
        uservoice_tickets.Uservoice_tickets(),
        uservoice_suggestions.Uservoice_suggestions(),
        rescuetime.Rescuetime(),
        github.Github(),
        gmail.Gmail()
    ],
    "latest": [
        hourly_uniques.Hourly_uniques(),
        latestprofile.LatestProfile()
    ],
    "scale": [
        products_per_profile.Products_per_profile(),
        daily_new_users.Daily_new_users(),
        daily_api_calls.Daily_api_calls(),
        profiles_per_genre.Profiles_per_genre(),
        importers_used.Importers_used()
    ],
    "totals":[
        itemsbycreateddate.ItemsByCreatedDate(),
        api_keys_minted.Api_keys_minted(),
        products_per_profile.Products_per_profile()
    ],
    "api": [
        embedded_widget_use.Embedded_widget_use(),
        api_key_item_creates.Api_key_item_creates(),
        api_key_item_views.Api_key_item_views()
    ],
    "health": [
        papertrail_alerts.Papertrail_alerts(),
        javascript_errors.Javascript_errors(),
        provider_requests.Provider_requests(),
        profile_load_times.Profile_load_times()
    ]
}


# add all the js to the page.
base_js = [
    'js_libs/jquery.sparkline.js',
    'js_libs/underscore.js',
    'js_libs/d3.min.js',
    'js_libs/d3.layout.min.js',
    'js_libs/rickshaw.js',
    'js_libs/icanhaz.js',
    'js_libs/moment.min.js',
    'dashboard.js'
]
base_css = [
    'css/rickshaw.css',
    'css/dashboard.css'
]
assets = Environment(app)

for k, v in dashboards.iteritems():
    for widget in v:

        base_js.append("js_widgets/" + widget.get_js_name_lower() + ".js")

assets.register('js_all', Bundle(*base_js))
assets.register('css_all', Bundle(*base_css))




# views

@app.before_request
def load_dashboards_list():
    g.dashboards = dashboards


# static pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon_ico():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route("/widget_data/<widget_name>")
def widget_data(widget_name):
    module = sys.modules["impactstoryanalytics.widgets." + widget_name.lower()]  # hack, ick
    class_name = widget_name[0].capitalize() + widget_name[1:]
    widget = getattr(module, class_name)()

    resp = make_response(json.dumps(widget.get_data(), indent=4), 200)
    resp.mimetype = "application/json"
    return resp


@app.route("/webhook/<source>", methods=['POST'])
def webhook(source):
    logger.info("got webhook from " + source.upper())

    if source == "errorception":
        # example whole post: {"isInline":true,"message":"Uncaught TypeError: Cannot call method 'split' of undefined","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36","when":"before","scriptPath":null,"page":"http://impactstory.org/faq","date":"2013-07-24T03:44:01.611Z","isFirstOccurrence":false,"webUrl":"http://errorception.com/projects/51ef3db2db2bef20770003e2/errors/51ef4d2114fb556e3de3f3d2","apiUrl":"https://api.errorception.com/projects/51ef3db2db2bef20770003e2/errors/51ef4d2114fb556e3de3f3d2"} 
        secret = os.getenv("ERRORCEPTION_SECRET", "")
        error_message = request.json.get("message", None)
        error_page = request.json.get("page", None)
        m = hashlib.sha1()
        m.update(secret + error_message + error_page)
        x_signature = request.headers.get("X-Signature")

        if x_signature == m.hexdigest():
            analytics.identify(user_id="WEBAPP")
            analytics.track("WEBAPP", "Caused a JavaScript error", request.json)

    elif source == "papertrail":
        alert_descriptions = {   
            "exception": "Threw an Exception", 
            "cant_start_new_thread": "Couldn't start a new thread", 
            "api_status_500": "Returned a server error from our API", 
            "unspecified": "Sent a Papertrail alert"
        }

        jsonstr = json.loads(request.form['payload']) #Load the Payload (Papertrail events)

        for event in jsonstr['events']: #Iterate through events
            message = "(" + event["display_received_at"] + ")" + " " + event["source_name"] + " " + event["program"] + " | " + event["message"] 
            logger.info("Brief version:" + message)
            logger.info("Full event:")
            logger.info(json.dumps(event, indent=4))

            if event["source_name"] in ["ti-core", "ti-webapp"]:
                app_name = event["source_name"].replace("ti-", "").upper()
                analytics.identify(user_id=app_name)
                alert_name = request.args.get("alert_name", "unspecified")
                analytics.track(app_name, alert_descriptions[alert_name], event)
            else:
                logger.info("Unknown event source_name, not sending")

    elif source == "email":
        # right now these are all from PAGERDUTY.  Do something smarter later.
        analytics.identify(user_id="PAGERDUTY")
        analytics.track("PAGERDUTY", "Alert from PagerDuty", request.json)

    else:
        logger.info("got webhook from a place we didn't expect")
        logger.info(source + " whole post: ")
        logger.info(request.data)

    resp = make_response(json.dumps({"source": source}, indent=4), 200)
    resp.mimetype = "application/json"
    return resp


@app.route('/<dashboard_name>')
def dashboard(dashboard_name):
    try:
        widgets = g.dashboards[dashboard_name]
    except AttributeError:
        redirect(url_for(dashboard, dashboard_name="main"))


    widget_names = [widget.get_name() for widget in widgets]

    return render_template(
        "dashboards/{name}.html".format(name=dashboard_name),
        current_dashboard_name=dashboard_name,
        widget_names=widget_names
    )


























