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

from impactstoryanalytics.widgets.widget import Widget, get_raw_keenio_data
import cache



logger = logging.getLogger("impactstoryanalytics.widgets.monthly_active_users")

class Daily_api_calls(Widget):

    api_calls_query_pattern = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Received%20API%20request%20from%20external&filters=%5B%7B%22property_name%22%3A%22api_key%22%2C%22operator%22%3A%22gt%22%2C%22property_value%22%3A%220%22%7D%2C%7B%22property_name%22%3A%22method%22%2C%22operator%22%3A%22eq%22%2C%22property_value%22%3A%22{method}%22%7D%5D&timeframe=last_30_days&target_property=api_key&interval=daily"

    def get_timestamp_from_isoformat(self, isodate):
        timestamp = int(time.mktime(iso8601.parse_date(isodate).timetuple()))
        return timestamp

    def get_dates_from_keenio(self, data):
        dates = [point["timeframe"]["start"] for point in data]
        return dates

    def get_values_from_keenio(self, data):
        dates = [int(point["value"]) for point in data]
        return dates

    def get_raw_data(self, number_of_bins):
        data = defaultdict(list)

        get_calls_query_url = self.api_calls_query_pattern.format(
            method = "GET")
        gets_data_from_keenio = get_raw_keenio_data(get_calls_query_url)
        data["dates"] = self.get_dates_from_keenio(gets_data_from_keenio)

        data["timestamps"] = [self.get_timestamp_from_isoformat(date) for date in data["dates"]]
        data["gets"] = self.get_values_from_keenio(gets_data_from_keenio)

        post_calls_query_url = self.api_calls_query_pattern.format(
            method = "POST")
        posts_data_from_keenio = get_raw_keenio_data(post_calls_query_url)
        data["posts"] = self.get_values_from_keenio(posts_data_from_keenio)

        return data


    def get_data(self):
        number_of_bins = 30  #show 30 days worth
        data = self.get_raw_data(number_of_bins)

        response = [{ 
                        "display": "GETs",
                        "name": "GETs",
                        "x": data["timestamps"], 
                        "y": data["gets"]
                    },
                    { 
                        "display": "POSTs",
                        "name": "POSTs",
                        "x": data["timestamps"], 
                        "y": data["posts"]
                    }] 
        return response