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
import cache

from impactstoryanalytics.lib import mixpanel_export

logger = logging.getLogger("impactstoryanalytics.external_providers")


## Utility functions
def get_raw_dataclip_data(query_url):
    #example query_url: "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    raw_data = requests.get(query_url).json()
    #print raw_data
    return raw_data

def get_raw_keenio_data(query_url):
    raw_data = requests.get(query_url).json()["result"]
    return raw_data



class Mixpanel():

    @classmethod
    def get_funnel_data(cls, api, funnel, funnel_params):
        logger.info("Getting funnel data for " + funnel["name"])

        funnel_params["funnel_id"] = funnel["funnel_id"]
        funnel_data = api.request(['funnels'], funnel_params)

        #print json.dumps(funnel_data, indent=4)

        logger.info("found data")

        return funnel_data["data"]

    @classmethod
    def get_funnels(cls, api):
        funnels = api.request(['funnels', 'list'], {})
        return funnels

    @classmethod
    def get_data(cls, funnel_name=None):

        api = mixpanel_export.Mixpanel(
            api_key = os.getenv("MIXPANEL_API_KEY"), 
            api_secret = os.getenv("MIXPANEL_API_SECRET")
        )

        funnels = cls.get_funnels(api)

        funnel_params = {
            # The first date in yyyy-mm-dd format from which a user can begin the first step in the funnel. This date is inclusive.
            "to_date": datetime.utcnow().isoformat()[0:10]  # today
            ,"from_date": (datetime.utcnow() - timedelta(days=7)).isoformat()[0:10]

            # The number of days each user has to complete the funnel, starting from the time they 
            # triggered the first step in the funnel. May not be greater than 60 days. 
            # Note that we will query for events past the end of to_date to look for funnel completions.
            #The default value is 14.
            ,"length": 1

            # The number of days you want your results bucketed into. The default value is 1
            ,"interval": 1
        }

        response = {}
        for funnel in funnels:

            if funnel_name:
                if (funnel_name != funnel["name"]):
                    continue

            response[funnel["name"]] = cls.get_funnel_data(api, funnel, funnel_params)

        return response

       
