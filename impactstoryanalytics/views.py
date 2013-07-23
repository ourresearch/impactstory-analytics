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
from impactstoryanalytics.widgets import rescuetime
from impactstoryanalytics.widgets import gmail
from impactstoryanalytics.widgets import github
from impactstoryanalytics.widgets import latestprofile
from impactstoryanalytics.widgets import itemsbycreateddate
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
        monthly_active_users.Monthly_active_users(),
    ],
    "productivity": [
        rescuetime.Rescuetime(),
        gmail.Gmail(),
        github.Github()
    ],
    "latest": [
        latestprofile.LatestProfile()
    ],
    # "scale": [
    #     itemsbycreateddate.ItemsByCreatedDate()
    # ],
    "totals": [
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
    active_users_keenio_query = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Viewed%20own%20profile&filters=%5B%7B%22property_name%22%3A%22days_since_account_created%22%2C%22operator%22%3A%22gte%22%2C%22property_value%22%3A1%7D%5D&timeframe=this_week&timezone=US%2FPacific&target_property=user.traits.email&interval=daily"

    keenio_data = requests.get(active_users_keenio_query).json()["result"]
    timepoints = [datapoint["timeframe"]["start"] for datapoint in keenio_data]
    values = [datapoint["value"] for datapoint in keenio_data]

    date_format = "%b %d"  # Mar 10
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




@app.route("/rescuetime/<first_name>")
def rescuetime_endpoint(first_name):
    data = rescuetime.get_data(first_name)
    dayslist = rescuetime.list_activity_by_day(data)

    chart = highcharts.streamgraph()
    chart["xAxis"] = {
        "categories": [day["name"] for day in dayslist]
    }
    chart["yAxis"]["max"] = 15
    colors = [  # these will stack in this same order on the graph
        ("other", "#666666"),
        ("email", "#D7191C"),
        ("code", "#1A9641")
    ]
    for series_name, color in colors:
        this_series = {
            "data": [round(day[series_name], 1) for day in dayslist],
            "name": series_name,
            "color": color
        }
        chart["series"].append(this_series)

    resp = make_response(highcharts.as_js(chart), 200)
    resp.mimetype = "application/x-javascript"

    return resp


@app.route("/uservoice-tickets")
def uservoice_tickets():
    from impactstoryanalytics import uservoice_check
    (num_all_tickets, num_last_response_was_a_user) = uservoice_check.get_ticket_counts()

    gecko_response = {"item":[
        {"text":"","value":num_all_tickets},
        {"text":"","value":num_last_response_was_a_user}]}

    resp = make_response(json.dumps(gecko_response, indent=4), 200)
    resp.mimetype = "application/json"
    return resp


@app.route("/widget_data/<widget_name>")
def widget_data(widget_name):
    module = sys.modules["impactstoryanalytics.widgets." + widget_name.lower()]  # hack, ick
    class_name = widget_name[0].capitalize() + widget_name[1:]
    widget = getattr(module, class_name)()

    resp = make_response(json.dumps(widget.get_data(), indent=4), 200)
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


























