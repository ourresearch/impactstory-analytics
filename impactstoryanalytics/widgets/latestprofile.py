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

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
import cache



logger = logging.getLogger("impactstoryanalytics.widgets.latestprofile")


class LatestProfile(Widget):
    dataclip_url = "https://dataclips.heroku.com/nhkmopcglhvmyoepqlxtxyxiewfj.json"

    def get_data(self):
        values = get_raw_dataclip_data(self.dataclip_url)["values"][0]
        return {
            "date": values[0] + "+00:00",  # dates go out in UTC
            "url": values[1]
        }





