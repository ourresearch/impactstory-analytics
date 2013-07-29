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
from impactstoryanalytics.widgets.widget_api_helpers import Uservoice

import cache



logger = logging.getLogger("impactstoryanalytics.widgets.uservoice_suggestions_upvoted")

class Uservoice_suggestions_upvoted(Widget):
    def get_data(self):
        suggestions = Uservoice.get_suggestion_details()

        fields = [
            "title",
            "url",
            "created_at",
            "vote_count",
            "subscriber_count"
            ]
        response = [{field: suggestion[field] for field in fields} for suggestion in suggestions]
        response.sort(key=lambda x:(x['vote_count']), reverse=True)
        for suggestion in response:
            suggestion["start_iso"] = suggestion["created_at"]
            del suggestion["created_at"]

        print json.dumps(response, indent=4)

        return response


        