from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.lib import gmail_oauth2
import imaplib
import re



class Gmail(Widget):

    query_url = "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries/minimum?api_key=b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e&event_collection=Inbox%20check&timeframe=this_48_hours&timezone=-25200&target_property=thread_count&group_by=userId&interval=hourly"

    def get_data(self):
        return {"foo": "bar"}


    def get_raw_data(self):
        raw_data = requests.get(self.query_url).json()["result"]
        return raw_data


    def inbox_threads(self):

        raw_data = self.get_raw_data()
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









