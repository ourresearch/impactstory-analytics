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

from impactstoryanalytics.widgets import widgets
from impactstoryanalytics.widgets.widgets import Widget

import external_providers
import cache



logger = logging.getLogger("impactstoryanalytics.widgets.itemsbycreateddate")


class ItemsCount():
    total = 0
    registered = 0
    cum_total = 0
    cum_registered = 0
    d = None

    def set_or_zero(self, k, dict):
        try:
            return dict[k]
        except KeyError:
            return 0

    def set_counts_from_dict(self, type, k, dict):    # "type" can be 'total' or 'registered'
        num = self.set_or_zero(k, dict)
        setattr(self, type, num)
        self.add_to_cum(num, type)

    def add_to_cum(self, num_to_add, type):
        property_str = "cum_" + type
        current_val = getattr(self, property_str)
        new_val = current_val + num_to_add
        setattr(self, property_str, new_val)

    def get_dict(self):
        return {
            "date": self.d.isoformat(),
            "total": self.total,
            "registered": self.registered,
            "unregistered": self.total - self.registered,
            "cum_total": self.cum_total,
            "cum_registered": self.cum_registered,
            "cum_unregistered": self.cum_total - self.cum_registered
        }



class ItemsByCreatedDate(Widget):
    couch_query = "_design/dashboard/_view/items_by_day_created?reduce=true&group=true"
    registered_items_url = "https://dataclips.heroku.com/btawwfbgqkmuzkkstbvlrqfyjqzz.json"

    def get_point(self, k, table):
        try:
            return table[k]
        except KeyError:
            return 0


    def get_data(self):
        items_by_day = {
            "total": self.get_total_items_by_day(),
            "registered": self.get_registered_items_by_day()
        }

        first_day_str = sorted(items_by_day["total"].keys())[0]
        first_day = arrow.get(str(first_day_str), 'YYYY-MM-DD')

        days = []
        day = ItemsCount()

        for r in arrow.Arrow.range("day", first_day, arrow.get()):
            day.d = r
            day_key = r.isoformat()[0:10]
            day.set_counts_from_dict(
                "total",
                day_key,
                items_by_day["total"]
            )
            day.set_counts_from_dict("registered",
                day_key,
                items_by_day["registered"]
            )

            days.append(day.get_dict())


        return days



    def make_days_dict(self, start_date):
        d = datetime.utcnow()
        days_dict = {}
        for _ in xrange(0, 50):
            days_dict[self.beginning_of_day_ts(d)] = 0
            d -= timedelta(days=1)


    def get_total_items_by_day(self):
            url = "/".join([
                os.getenv("CLOUDANT_URL"),
                os.getenv("CLOUDANT_DB"),
                self.couch_query
            ])

            items_by_day = requests.get(url).json()["rows"]
            ret = {}
            for day in items_by_day:
                ret[day["key"]] = day["value"]

            return ret

    def get_registered_items_by_day(self):
        raw_data = get_raw_dataclip_data(self.registered_items_url)
        ret = {}
        for datapoint in raw_data["values"]:
            short_date = datapoint[0][0:10]
            ret[short_date] = int(datapoint[1])

        return ret

