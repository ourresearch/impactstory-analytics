import time
from datetime import timedelta
from datetime import date
from datetime import datetime
import requests
import iso8601
import os
import logging
import pytz


logger = logging.getLogger("impactstoryanalytics.widgets")


## Utility functions
def get_raw_dataclip_data(query_url):
    #example query_url: "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    raw_data = requests.get(query_url).json()
    #print raw_data
    return raw_data

def get_raw_keenio_data(query_url):
    raw_data = requests.get(query_url).json()["result"]
    return raw_data





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
    issue_q_url_template = "https://api.github.com/repos/total-impact/total-impact-{NAME}/issues"
    num_days = 31
    repo_names = ["webapp", "core"]

    def get_data(self):
        lines = {}
        for repo_name in self.repo_names:
            issues_list = self.get_raw_data_repo(repo_name)
            line = self.make_line(issues_list)
            lines[repo_name] = line.values()

        # zipped = zip(*lines.values())
        return lines


    def get_both_closed_and_open_issues(self, q_url):
        issues = []
        tz = pytz.timezone(os.getenv("TZ"))
        begin = (datetime.now(tz) - timedelta(days=self.num_days))
        params = {
            "since": begin.isoformat(),
            "state": "open"
        }
        logger.info("querying github with url " + q_url)
        issues = requests.get(q_url, params=params).json()

        return issues

    def get_raw_data_repo(self, repo_name):
        q_url = self.issue_q_url_template.format(NAME=repo_name)
        return self.get_both_closed_and_open_issues(q_url)

    def beginning_of_day_ts(self, datetime_obj):
        d = datetime_obj.replace(hour=0, minute=0, second=0)
        return str(d.isoformat()[0:10])

    def make_line(self, issues_list):
        d = datetime.utcnow()
        days_list = {}
        for _ in xrange(0, 50):
            days_list[self.beginning_of_day_ts(d)] = 0
            d -= timedelta(days=1)

        logger.info("days list is this: " + str(sorted(days_list.keys())))

        for issue in issues_list:
            d = iso8601.parse_date(issue["created_at"])

            try:
                days_list[self.beginning_of_day_ts(d)] += 1
            except KeyError:
                continue  # it's not in our window of interest

        return days_list



class Mixpanel(Widget):

    total_accounts_query_url = "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    #active_accounts_query_url = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Loaded%20own%20profile&filters=%5B%7B%22property_name%22%3A%22keen.timestamp%22%2C%22operator%22%3A%22lt%22%2C%22property_value%22%3A%222013%2F07%2F17%22%7D%2C%7B%22property_name%22%3A%22keen.timestamp%22%2C%22operator%22%3A%22gt%22%2C%22property_value%22%3A%222013%2F06%2F17%22%7D%5D&target_property=user.userId"
    active_accounts_query_pattern = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Loaded%20own%20profile&filters=%5B%7B%22property_name%22%3A%22keen.created_at%22%2C%22operator%22%3A%22lt%22%2C%22property_value%22%3A%22{from_date}%22%7D%2C%7B%22property_name%22%3A%22keen.created_at%22%2C%22operator%22%3A%22gte%22%2C%22property_value%22%3A%22{to_date}%22%7D%5D&target_property=user.userId"

    def format_date(self, date):
        date_only = date.isoformat()[0:10]
        #escaped_date = date_only.replace("-", "%2F")
        return date_only

    def get_raw_data(self, number_of_bins):
        data = {
            "timestamp_list": [],
            "total_account_list": [],
            "active_account_list": [],
            "fraction_list": [],
        }

        total_accounts = get_raw_dataclip_data(self.total_accounts_query_url)

        for datapoint in total_accounts["values"][0:number_of_bins]:
            (date, new_accounts, total_accounts) = datapoint

            from_date = iso8601.parse_date(date)
            to_date = from_date - timedelta(days=30)

            active_accounts_query_url = self.active_accounts_query_pattern.format(
                from_date = self.format_date(from_date), 
                to_date = self.format_date(to_date))

            active_accounts = get_raw_keenio_data(active_accounts_query_url)
            data["timestamp_list"].append(int(time.mktime(from_date.timetuple())))
            data["total_account_list"].append(int(total_accounts))
            data["active_account_list"].append(int(active_accounts))
            data["fraction_list"].append((0.0+int(active_accounts))/int(total_accounts))

        return data


    def get_data(self):
        number_of_bins = 7  # eventually make this 30 days
        data = self.get_raw_data(number_of_bins)
        return {"fraction": {"x": data["timestamp_list"], "y": data["fraction_list"]}}


