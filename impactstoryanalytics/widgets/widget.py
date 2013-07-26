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

import cache



logger = logging.getLogger("impactstoryanalytics.widget")


## Utility functions
def get_raw_dataclip_data(query_url):
    #example query_url: "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    raw_data = requests.get(query_url).json()
    #print raw_data
    return raw_data

def get_raw_keenio_data(query_url):
    raw_data = requests.get(query_url).json()["result"]
    return raw_data


class TimePansList:
    def __init__(self, pans=None):
        self.pans = []
        if pans is not None:
            self.pans += pans

    def as_list(self):
        ret = []
        for pan in self.pans:
            ret.append(pan.as_dict())

        return ret

    def add_pan(self, pan):
        self.pans.append(pan)

    def add_to_pan(self, time, k, v):
        pan = self.find_pan_from_time(time)
        pan.dict[k] += v

    def find_pan_from_time(self, time):
        for pan in self.pans:
            if time > pan.start and time < pan.end:
                return pan



class TimePan:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.dict = defaultdict(int)

    def as_dict(self):
        dict = self.dict
        dict["start_iso"] = self.start.isoformat(" ")
        dict["end_iso"] = self.end.isoformat(" ")
        return dict


class Widget:
    def get_name(self):
        return self.__class__.__name__

    def get_js_name_lower(self):
        name = self.__class__.__name__
        return name[0].lower() + name[1:]

    def get_data(self):
        raise NotImplementedError

    def get_time_pan_list(self, num_bins, interval="day"):
        end = arrow.utcnow().ceil("day")  # end of today
        start = end.floor("day").replace(days=-num_bins)
        pans = TimePansList()
        for r in arrow.Arrow.span_range(interval, start, end):
            new_pan = TimePan(r[0], r[1])
            pans.add_pan(new_pan)

        return pans









