from datetime import timedelta
from datetime import datetime
from collections import defaultdict
import requests
import os
import logging

from impactstoryanalytics.lib import mixpanel_export
import uservoice

logger = logging.getLogger("impactstoryanalytics.widget_api_helpers")


## Utility functions
def get_raw_dataclip_data(query_url):
    #example query_url: "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    raw_data = requests.get(query_url).json()
    #print raw_data
    return raw_data

def get_raw_keenio_data(query_url):
    raw_data = requests.get(query_url).json()["result"]
    return raw_data


class Keenio():
    queries = {}
    timebins = defaultdict(dict)
    params = {
        "timeframe": "last_30_days",
        "interval": "daily"
    }
    timeframe = "last_30_days"
    interval = "day"

    def __init__(self, queries):
        for q_name, q_url in queries.iteritems():
            self.queries[q_name] = q_url

    def get_raw_data(self):
        for q_name, q_url in self.queries.iteritems():
            r = requests.get(q_url, params=self.params)
            print r.text

            raw_data = r.json()["result"]

            for row_from_keen in raw_data:
                new_row = self.create_row(row_from_keen, q_name)
                self.timebins[new_row["start_iso"]].update(new_row)

        return self.timebins_as_list()




    def create_row(self, row_from_keen, value_name):
        return {
            "start_iso": row_from_keen["timeframe"]["start"],
            "end_iso": row_from_keen["timeframe"]["end"],
            value_name: row_from_keen["value"]
        }

    def timebins_as_list(self):
        ret = []
        for k in sorted(self.timebins.keys()):
            ret.append(self.timebins[k])

        return ret







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



class Uservoice():
    @classmethod
    def get_uservoice_owner(cls):
        SUBDOMAIN_NAME = 'impactstory'
        API_KEY = os.getenv("USERVOICE_API_KEY")
        API_SECRET = os.getenv("USERVOICE_API_SECRET")

        client = uservoice.Client(SUBDOMAIN_NAME, API_KEY, API_SECRET)
        owner = client.login_as_owner()
        return owner

    @classmethod
    def get_ticket_stats(cls, my_agent_name="Unassigned"):
        logger.info("Getting uservoice ticket stats")

        owner = cls.get_uservoice_owner()

        api_response = owner.get("/api/v1/reports/queue_backlog.json")

        interesting_fields = [
            "without_response_count", 
            "waiting_for_agent_count", 
            "total_count",
            "median_open_time"
            ]

        ticket_dict = {}
        for agent in api_response["entries"]:
            if agent["name"] == my_agent_name:
                for field in interesting_fields:
                    if field == "median_open_time":
                        ticket_dict["median_open_days"] = round(agent[field]/(60.0*60*24), 1)
                    else:
                        ticket_dict[field] = agent[field]

        logger.info("Found uservoice tickets: {all} total, {user} where a user answered last".format(
            all=ticket_dict["total_count"], 
            user=ticket_dict["waiting_for_agent_count"]))

        return ticket_dict


    @classmethod
    def get_ticket_details(cls):
        logger.info("Getting uservoice ticket details")

        owner = cls.get_uservoice_owner()
        tickets = owner.get("/api/v1/tickets?state=open&per_page=100")["tickets"]

        return tickets


    @classmethod
    def get_suggestion_counts(cls):
        logger.info("Getting uservoice suggestion count")

        owner = cls.get_uservoice_owner()
        suggestions_active = owner.get("/api/v1/suggestions?filter=active&per_page=1000")["suggestions"]
        suggestions_inbox = owner.get("/api/v1/suggestions?filter=inbox&per_page=1000")["suggestions"]
        suggestions = suggestions_active + suggestions_inbox

        suggestion_dict = {}
        for suggestion in suggestions:
            status = "inbox"
            if suggestion["status"]:
                status = suggestion["status"]["name"]
            suggestion_dict[status] = 1 + suggestion_dict.get(status, 0)

        logger.info("Found uservoice suggestions: {total} total".format(
            total=len(suggestions)))

        return(suggestion_dict)

       
