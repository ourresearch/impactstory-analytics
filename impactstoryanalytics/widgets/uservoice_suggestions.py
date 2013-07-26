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

import cache



logger = logging.getLogger("impactstoryanalytics.widgets.uservoice_suggestions")

class Uservoice_suggestions(Widget):
    def get_data(self):
        target_properies = [
                    "started", 
                    "under_review", 
                    "planned", 
                    "inbox"
                ]
        queries = {}
        for target_property in target_properies:
            queries[target_property] = {
                    "project": "context",
                    "analysis": "minimum",
                    "params": {"target_property": target_property}
                }

        shared_params = {
                    "event_collection" : "UserVoice suggestions",
                    "timeframe": "this_30_days",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


        