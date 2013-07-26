from collections import defaultdict
from collections import Counter
import requests
import logging
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
        for pan in self.pans:
            if pan.start <= time < pan.end:
                pan.dict[k] += v
                return True

    def replace_NAs_with_zeroes(self):
        keys = self.list_all_pan_keys()
        for pan in self.pans:
            pan.pad_keys(keys)

        return self

    def add_cum_counts(self):
        counter = Counter()
        for pan in self.pans:
            # update the cumulative totals for each dict key
            counter.update(pan.as_dict(counts_only=True))

            # put the current cumlative totals in the pan's dict
            for k, count in counter.iteritems():
                pan.dict["cum_" + k] = count

        return self



    def list_all_pan_keys(self):
        extant_keys = []
        for pan in self.pans:
            extant_keys += pan.dict.keys()

        return list(set(extant_keys))








class TimePan:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.dict = defaultdict(int)

    def as_dict(self, counts_only=False):
        dict = self.dict
        dict["start_iso"] = self.start.isoformat(" ")
        dict["end_iso"] = self.end.isoformat(" ")

        if counts_only:
            dict = {}
            for k, v in self.dict.iteritems():
                try:
                    dict[k] = v + 0  # make sure it's a number
                except TypeError:
                    pass

        return dict

    def pad_keys(self, keys):
        """
        Add keys with zero values if they don't exist in the dict
        """
        for key in keys:
            self.dict.setdefault(key, 0)




class Widget:
    def get_name(self):
        return self.__class__.__name__

    def get_js_name_lower(self):
        name = self.__class__.__name__
        return name[0].lower() + name[1:]

    def get_data(self):
        raise NotImplementedError

    @classmethod
    def get_time_pan_list(cls, num_bins, interval="day"):
        end = arrow.utcnow().ceil("day")  # end of today
        start = end.floor("day").replace(days=-num_bins)
        pans = TimePansList()
        for r in arrow.Arrow.span_range(interval, start, end):
            new_pan = TimePan(r[0], r[1])
            pans.add_pan(new_pan)

        return pans









