import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter



logger = logging.getLogger("impactstoryanalytics.widgets.signup_growth_target")


class Signup_growth_target(Widget):
    query = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo"
