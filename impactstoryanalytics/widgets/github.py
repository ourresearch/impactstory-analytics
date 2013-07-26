from datetime import timedelta
from datetime import datetime
import requests
import logging
import arrow
from impactstoryanalytics.widgets.widget import Widget

logger = logging.getLogger("impactstoryanalytics.widgets.github")


class Github(Widget):

    def __init__(self):
        self.issue_q_url_template = "https://api.github.com/repos/total-impact/total-impact-{NAME}/issues"
        self.repo_names = ["webapp", "core"]

    def get_data(self):
        pans = self.get_time_pan_list(30)

        for repo_name in self.repo_names:
            for open_issue in self.get_issues_list(repo_name, "open"):
                opened_time = arrow.get(str(open_issue["created_at"]), 'YYYY-MM-DDTHH:mm:ss')
                opened_name = repo_name + "_issues_open"
                pans.add_to_pan(opened_time, opened_name, 1)

            for closed_issue in self.get_issues_list(repo_name, "closed"):
                closed_time = arrow.get(str(closed_issue["closed_at"]), 'YYYY-MM-DDTHH:mm:ss')
                pans.add_to_pan(closed_time, "issues_closed", 1)

        return pans.replace_NAs_with_zeroes().as_list()


    def get_issues_list(self, repo_name, state):
        q_url = self.issue_q_url_template.format(NAME=repo_name)
        begin = (datetime.now() - timedelta(days=32))
        params = {
            "since": begin.isoformat(),
            "state": state
        }
        logger.info("querying github with url " + q_url)
        issues = requests.get(q_url, params=params).json()
        return issues



