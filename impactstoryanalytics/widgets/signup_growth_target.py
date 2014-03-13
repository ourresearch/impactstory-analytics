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
        self.signups_total_endpoints = {
            "start": 4255,
            "finish": 10000  # 10k
        }

    def get_data(self):

        dataclip_data = get_raw_dataclip_data(self.data_url)
        datapoints = [[p[0][0:10], p[2]] for p in dataclip_data["values"]]

        actual_line = {}
        for row in dataclip_data["values"]:
            day_str = row[0][0:10]
            actual_line[day_str] = [int(v) for v in row[1:]]


        target_line = self.make_target_line()

        rows = []
        for date in sorted(target_line.keys()):
            actual_values = actual_line.get(date, ["", ""])
            target_values = target_line[date]

            rows.append([date] + actual_values + target_values)

        fields = [
            "date",
            "actual_signups",
            "actual_signups_total",
            "target_signups",
            "target_signups_total"
        ]

        return {"fields": fields, "values": rows}



    def make_target_line(self):
        target_line = {}
        datapoint = {
            "date": self.start_date,
            "signups": "",
            "signups_total": self.signups_total_endpoints["start"]
        }

        while datapoint["signups_total"] < self.signups_total_endpoints["finish"]:

            # update the target line
            date_str = datapoint["date"].format('YYYY-MM-DD')
            target_line[date_str] = [
                datapoint["signups"],
                datapoint["signups_total"]
            ]

            # increment values for next iteration
            datapoint["date"] = datapoint["date"].replace(days=+1)
            datapoint["signups"] = self.daily_growth * datapoint["signups_total"]
            datapoint["signups_total"] *= (1 + self.daily_growth)



        return target_line






