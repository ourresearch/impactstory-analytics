import time
from datetime import timedelta
from datetime import datetime
import requests
import iso8601
import os
import logging


from impactstoryanalytics.widgets.widget import Widget



logger = logging.getLogger("impactstoryanalytics.widgets.rescuetime")


class Rescuetime(Widget):
    def get_data(self):
        heather_and_jason_activity = {}
        for user in ["Heather", "Jason"]:
            raw_data = self.get_raw_data(user)
            heather_and_jason_activity[user] = self.list_activity_by_day(raw_data)

        return heather_and_jason_activity



    def get_raw_data(self, user):

        env_key = "RESCUETIME_KEY_" + user.upper()
        rescuetime_api_key = os.getenv(env_key)

        params = {
            "key": rescuetime_api_key,
            "format": "json",
            "perspective": "interval",
            "resolution_time": "day",
            "restrict_kind": "category",
            "restrict_begin": datetime.utcnow() - timedelta(days=7),
            "restrict_end": datetime.utcnow() + timedelta(days=1)
        }
        url = "https://www.rescuetime.com/anapi/data"


        try:
            r = requests.get(url, params=params)
            data = r.json()["rows"]
        except ValueError:
            logger.debug(u"ValueError in get_raw_data with user {user} on request {url}".format(
                user=user, 
                url=r.url))
            data = []

        return data

    def is_code_category(self, category):
        code_categories = [
            "general software development",
            "design & planning",
            "editing & ides",
            "quality assurance",
            "systems operations",
            "data modeling & analysis"
        ]

        if category.lower() in code_categories:
            return True
        else:
            return False

    def list_activity_by_day(self, data):

        days = {}

        # initialize first so we make sure we have zeros for every day
        first_day = datetime.utcnow()
        for day in [first_day - timedelta(days=i) for i in range(8)]:
            # crazy hack to fix rescuetime rickshaw axis
            adj_data = day
            datestring = day.isoformat()[0:10] + "T00:00:00"

            timestamp = int(time.mktime(adj_data.timetuple()))
            days[datestring] = {
                "total": 0,
                "email": 0,
                "code": 0,
                "timestamp": timestamp
            }

        print days.keys()

        for row in data:
            datestring = row[0]
            time_spent = float(row[1]) / 3600  # in hours
            category = row[3]

            # add to the time counts for this day
            days[datestring]["total"] += time_spent
            if category == "Email":
                days[datestring]["email"] += time_spent
            elif self.is_code_category(category):
                days[datestring]["code"] += time_spent


        # now that all the data is in, calculate the "other" category
        for k, v in days.iteritems():
            v["other"] = v["total"] - (v["email"] + v["code"])

        # easier to work with a list
        dayslist = []
        for k in sorted(days.keys()):
            dayslist.append(days[k])

        # convert to the format Rickshaw likes
        categories = {"other": [], "email": [], "code": []}
        for category_name, category_values in categories.iteritems():
            for index, day in enumerate(dayslist):
                datapoint = {
                    "x": index,
                    "y": day[category_name]
                }
                category_values.append(datapoint)




        return categories

