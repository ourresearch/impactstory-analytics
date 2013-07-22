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

from impactstoryanalytics.widgets.widget import Widget
import cache



logger = logging.getLogger("impactstoryanalytics.widgets.github")


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


