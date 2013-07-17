import time
from datetime import timedelta
from datetime import date
import requests
import iso8601
import os
import logging
import numpy as np

logger = logging.getLogger("impactstoryanalytics.widgets")


class Widget:
    def get_name(self):
        return self.__class__.__name__.lower()

    def get_data(self):
        raise NotImplementedError

    def make_day_bins(self, num_days):
        pass




class Gmail(Widget):

    query_url = "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries/minimum?api_key=b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e&event_collection=Inbox%20check&timeframe=this_48_hours&timezone=-25200&target_property=thread_count&group_by=userId&interval=hourly"

    def get_data(self):
        return self.inbox_threads()


    def get_raw_data(self):
        raw_data = requests.get(self.query_url).json()["result"]
        return raw_data


    def inbox_threads(self):

        raw_data = self.get_raw_data()
        lines = {
            "Heather": [],
            "Jason": []
        }

        for this_bin in raw_data:
            bin_start_time = iso8601.parse_date(this_bin["timeframe"]["start"])
            adj_start_time = bin_start_time

            for val in this_bin["value"]:
                if val["result"] is not None:
                    datapoint = {
                        "x": int(time.mktime(adj_start_time.timetuple())),
                        "y": val["result"]
                    }

                    lines[val["userId"]].append(datapoint)


        return lines










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
            "restrict_begin": date.today() - timedelta(days=6),
            "restrict_end": date.today() + timedelta(days=1)
        }
        url = "https://www.rescuetime.com/anapi/data"


        data = requests.get(url, params=params).json()["rows"]
        return data

    def is_code_category(self, category):
        code_categories = [
            "general software development",
            "design & planning",
            "editing & ides",
            "quality assurance",
            "systems operations",
            "data modelling and analysis"
        ]

        if category.lower() in code_categories:
            return True
        else:
            return False

    def list_activity_by_day(self, data):

        days = {}
        for row in data:
            datestring = row[0]
            time_spent = float(row[1]) / 3600  # in hours
            category = row[3]

            # add this day if we don't have it yet
            if datestring not in days:
                # crazy hack to fix rescuetime rickshaw axis
                adj_data = iso8601.parse_date(datestring)

                timestamp = int(time.mktime(adj_data.timetuple()))
                days[datestring] = {
                    "total": 0,
                    "email": 0,
                    "code": 0,
                    "timestamp": timestamp
                }

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



class Github(Widget):
    issue_q_url_template = "https://api.github.com/repos/total-impact/total-impact-{NAME}"
    num_days = 31
    repo_names = ["webapp", "core"]

    def get_data(self):
        return self.get_raw_data()

    def get_both_closed_and_open_issues(self, q_url):
        issues = []
        params = {
            "since": date.today() - timedelta(days=self.num_days)
        }
        for state in ["closed", "open"]:
            params["state"] = state
            logger.info("querying github with url " + q_url)
            issues += requests.get(q_url, params=params).json()

        return issues

    def get_raw_data(self):
        raw_data = {}
        for repo_name in self.repo_names:
            q_url = self.issue_q_url_template.format(NAME=repo_name)
            raw_data[repo_name] = self.get_both_closed_and_open_issues(q_url)

        return raw_data