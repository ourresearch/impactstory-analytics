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

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.daily_api_calls")


class Daily_api_calls(Widget):

    def get_data(self):
        methods = ["GET", "POST"]
        queries = {}
        for method in methods:
            filter_pattern = '[{"property_name":"api_key","operator":"gt","property_value":"0"},{"property_name":"method","operator":"eq","property_value":"%s"}]'
            filter_string = filter_pattern %method
            queries[method] = {
                    "project": "production",
                    "analysis": "count",
                    "params": {"filters": filter_string}
                }

        shared_params = {
                    "event_collection" : "Received API request from external",
                    "timeframe": "this_30_days",
                    "target_property": "api_key",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


