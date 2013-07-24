import requests
import os
import sys
import json
import logging
import iso8601
from impactstoryanalytics import app
from impactstoryanalytics import widgets
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
from impactstoryanalytics.widgets import uservoice_suggestions
from impactstoryanalytics.widgets.widget import Widget

from flask import request, abort, make_response, g, redirect, url_for
from flask import render_template
from flask.ext.assets import Environment, Bundle

logger = logging.getLogger("impactstoryanalytics.views")

# define dashboards
dashboards = {
    "main": [
        signup_growth.Signup_growth(),
        signup_funnel.Signup_funnel(),
        monthly_active_users.Monthly_active_users()
    ],
    "productivity": [
        uservoice_tickets.Uservoice_tickets(),
        uservoice_suggestions.Uservoice_suggestions(),
        rescuetime.Rescuetime(),
        gmail.Gmail(),
        github.Github()
    ],
    "latest": [
        latestprofile.LatestProfile()
    ],
    "scale": [
        daily_new_users.Daily_new_users(),
        daily_api_calls.Daily_api_calls()
    ],
    "totals":[
        itemsbycreateddate.ItemsByCreatedDate()
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
        dashboard_name=dashboard_name,
        widget_names=widget_names
    )


























