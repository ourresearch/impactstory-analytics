import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter



logger = logging.getLogger("impactstoryanalytics.widgets.signup_growth_target")


class Signup_growth_target(Widget):
    data_url = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo.json"

    """
        12 weeks till mayday (84 days)
        4331 users now
        5669 users needed to 10k
        in 112 days, that means about 5.5% growth per week
        which is also about .77% growth per day.

    """

    def get_data(self):

        dataclip_data = get_raw_dataclip_data(self.data_url)
        values = dataclip_data["values"]

        return dataclip_data