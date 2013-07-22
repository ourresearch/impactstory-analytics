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

from impactstoryanalytics.widgets.widgets import Widget

import external_providers
import cache



logger = logging.getLogger("impactstoryanalytics.widgets.signup_funnel")


class Signup_funnel(Widget):
    def get_data(self):
        return external_providers.Mixpanel.get_data("omtm")
