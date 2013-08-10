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


logger = logging.getLogger("impactstoryanalytics.widgets.uservoice_suggestions")

class Uservoice_suggestions(Widget):
    def get_data(self):

        pans = Widget.get_time_pan_list(30)

        suggestion_dict = Uservoice.get_closed_suggestion_count()

        for closed_suggestion in suggestion_dict:
            start_iso = arrow.get(str(closed_suggestion["closed_at"]), 'YYYY-MM-DDTHH:mm:ss')
            pans.add_to_pan(start_iso, "suggestions_closed", 1)

        return pans.replace_NAs_with_zeroes().as_list()


        