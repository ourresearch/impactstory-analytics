import requests
import os
import sys
import json
import logging
import iso8601
from impactstoryanalytics import app, highcharts, rescuetime
from impactstoryanalytics.widgets import gmail, rescuetime

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


@app.route("/inbox-threads")
def inbox_threads():
    keenio_q = "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries/minimum?api_key=b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e&event_collection=Inbox%20check&timeframe=this_48_hours&timezone=-25200&target_property=thread_count&group_by=userId&interval=hourly"
    keenio_data = requests.get(keenio_q).json()["result"]
    lines = {
        "Heather": [],
        "Jason": []
    }


    for this_bin in keenio_data:
        bin_start_time = iso8601.parse_date(this_bin["timeframe"]["start"])
        js_date = "Date.UTC({year}, {month}, {day}, {hour}, {minute})".format(
            year=bin_start_time.year,
            month=bin_start_time.month - 1,  # js wants jan to be 0. nice one.
            day=bin_start_time.day,
            hour=bin_start_time.hour,
            minute=bin_start_time.minute
        )
        for val in this_bin["value"]:
            if val["result"] is not None:
                point_def = [
                    js_date,
                    val["result"]
                ]

                lines[val["userId"]].append(point_def)

    chart = highcharts.timeseries_line()
    chart["series"] = [
        {"data": lines["Jason"], "color": "#EF8A62", "name": "Jason"},
        {"data": lines["Heather"], "color": "#67A9CF", "name": "Heather"}
    ]

    resp = make_response(highcharts.as_js(chart), 200)
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



@app.route("/dashboard/<dashboard_name>")
def dashboard(dashboard_name):

    if dashboard_name == "productivity":
        widget_names = [
            "gmail"
        ]

    elif dashboard_name == "main":
        # there's some other set of widget names
        pass

    else:
        redirect("/dashboard/main")


    widgets = []
    for widget_name in widget_names:
        module = sys.modules["impactstoryanalytics.widgets." + widget_name]  # hack, ick
        class_name = widget_name.capitalize()
        new_widget = getattr(module, class_name)()

        widgets.append(new_widget)




    return render_template(
        'dashboard.html',
        dashboard_name=dashboard_name,
        js_data={widget.get_name(): widget.get_data() for widget in widgets}
    )


























