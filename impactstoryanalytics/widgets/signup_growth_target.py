import time
from collections import defaultdict
import iso8601
import logging
import arrow

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter



logger = logging.getLogger("impactstoryanalytics.widgets.signup_growth_target")


class Signup_growth_target(Widget):
    signups_with_products_url = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo.json"
    raw_signups_data_url = "https://dataclips.heroku.com/qaclkwteaqnrltwxojgzytkgwczs.json"

    def __init__(self):
        Widget.__init__(self)
        self.start_date = arrow.get("2014-02-03")
        self.daily_growth = .0073  # times 7 = 5.11% weekly
        self.signups_total_endpoints = {
            "start": 4255,
            "finish": 10000  # 10k
        }

    def get_data(self):

        signups_with_products_data = get_raw_dataclip_data(self.signups_with_products_url)
        raw_signups_dataclip_data = get_raw_dataclip_data(self.raw_signups_data_url)

        actual_line = {}

        # make the raw signups line
        for row in raw_signups_dataclip_data["values"]:
            day_str = row[0][0:10]
            actual_line[day_str] = [int(row[1])]


        # make the signups-with-products line
        for row in signups_with_products_data["values"]:
            day_str = row[0][0:10]
            actual_line[day_str].append(int(row[1]))


        target_line = self.make_target_line()

        rows = []
        for date in sorted(target_line.keys()):
            actual_values = actual_line.get(date, ["", ""])
            target_values = target_line[date]

            rows.append([date] + actual_values + target_values)

        fields = [
            "date",
            "signups_raw",
            "signups_with_products",
            "target_signups_with_products",
            "target_signups_with_products_total"
        ]

        return {"fields": fields, "values": rows}

    def get_signup_line(self):
        pass





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






