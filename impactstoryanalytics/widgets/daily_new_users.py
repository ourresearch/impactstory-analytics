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



logger = logging.getLogger("impactstoryanalytics.widgets.monthly_active_users")

class Daily_new_users(Widget):

    new_accounts_query_url = "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"

    def format_date(self, date):
        date_only = date.isoformat()[0:10]
        return date_only

    def get_raw_data(self, number_of_bins):
        data = defaultdict(list)

        accounts_data = get_raw_dataclip_data(self.new_accounts_query_url)

        datapoints = accounts_data["values"][0:number_of_bins]
        # javascript currently expects data with most recent data last
        datapoints.reverse()

        for datapoint in datapoints:
            (date, new_accounts, total_accounts) = datapoint
            from_date = iso8601.parse_date(date)

            data["timestamp_list"].append(int(time.mktime(from_date.timetuple())))
            data["new_accounts"].append(int(new_accounts))

        return data


    def get_data(self):
        number_of_bins = 30  #show 30 days worth
        data = self.get_raw_data(number_of_bins)

        response = [{ 
                        "display": "new accounts",
                        "name": "new_accounts",
                        "x": data["timestamp_list"], 
                        "y": data["new_accounts"]
                        }]
        return response