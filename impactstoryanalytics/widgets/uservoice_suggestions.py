import time
from datetime import timedelta
from datetime import date
from datetime import datetime
from collections import defaultdict
import requests
import iso8601
import os
import logging
import pytz
import json
import arrow

from impactstoryanalytics.widgets.widget import Widget, get_raw_keenio_data
from impactstoryanalytics.widgets.widget_api_helpers import Uservoice

import cache



logger = logging.getLogger("impactstoryanalytics.widgets.uservoice_suggestions")

class Uservoice_suggestions(Widget):


    def get_timestamp_from_isoformat(self, isodate):
        timestamp = int(time.mktime(iso8601.parse_date(isodate).timetuple()))
        return timestamp

    def get_dates_from_keenio(self, data):
        dates = [point["timeframe"]["start"] for point in data]
        return dates

    def get_values_from_keenio(self, data):
        values = [point["value"] if point["value"] else 0 for point in data ]
        return values

    def get_data(self):
        data = []

        interesting_fields = [
            ("started", "started"), 
            ("under_review", "under review"), 
            ("planned", "planned"),
            ("inbox", "unfiled")
            ]

        for (name, display) in interesting_fields:
            chart = {}
            chart["name"] = name
            chart["display"] = display

            keenio_query_url_pattern = "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries/minimum?api_key=b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e&event_collection=UserVoice%20suggestions&timeframe=this_30_days&timezone=0&target_property={property}&interval=daily"
            keenio_query_url = keenio_query_url_pattern.format(property=name)

            keenio_data = get_raw_keenio_data(keenio_query_url)
            chart["y"] = self.get_values_from_keenio(keenio_data)

            # these overwrite every time, that's ok
            chart["dates"] = self.get_dates_from_keenio(keenio_data)
            chart["x"] = [self.get_timestamp_from_isoformat(date) for date in chart["dates"]]
            data.append(chart)

        return data



        