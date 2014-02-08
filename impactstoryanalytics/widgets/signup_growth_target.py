import time
from collections import defaultdict
import iso8601
import logging
import arrow

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter



logger = logging.getLogger("impactstoryanalytics.widgets.signup_growth_target")


class Signup_growth_target(Widget):
    data_url = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo.json"

    def __init__(self):
        Widget.__init__(self)
        self.start_date = arrow.get("2014-02-03")
        self.daily_growth = .0073  # times 7 = 5.11% weekly
        self.user_count = {
            "start": 4255,
            "finish": 10000  # 10k
        }

    def get_data(self):

        dataclip_data = get_raw_dataclip_data(self.data_url)
        datapoints = [[p[0][0:10], p[2]] for p in dataclip_data["values"]]


        actual_line = dict(datapoints)
        target_line = self.make_target_line()


        rows = []
        for date in sorted(target_line.keys()):
            actual_count = actual_line.get(date, None)
            target_count = target_line[date]
            rows.append([date, actual_count, target_count])

        return {"fields": dataclip_data["fields"], "values": rows}



    def make_target_line(self):
        target_line = {}
        datapoint = {
            "date": self.start_date,
            "count": self.user_count["start"]
        }

        while datapoint["count"] < self.user_count["finish"]:

            # update the target line
            date_str = datapoint["date"].format('YYYY-MM-DD')
            print "date string", date_str
            target_line[date_str] = datapoint["count"]

            # increment values for next iteration
            datapoint["date"] = datapoint["date"].replace(days=+1)
            datapoint["count"] *= (1 + self.daily_growth)



        return target_line






