from datetime import timedelta
from datetime import datetime
from collections import defaultdict
import requests
import os
import urllib
import logging
import arrow

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.lib import mixpanel_export
import uservoice

logger = logging.getLogger("impactstoryanalytics.widget_api_helpers")


## Utility functions
def get_raw_dataclip_data(query_url):
    #example query_url: "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"
    raw_data = requests.get(query_url).json()
    #print raw_data
    return raw_data

def perc(num, den, round_to=2):
    try:
        return round(100 * num / den, round_to)
    except ZeroDivisionError:
        return None


class Converter():
    @classmethod
    def from_x_y_format(cls, lines):
        events = defaultdict(dict)
        for line in lines:
            event_name = line["name"]
            new_events_dict = cls.events_dict_from_line(line)
            events = cls.merge_new_events_dict(events, new_events_dict, event_name)

        events_list = cls.events_list_from_dict(events)
        return events_list


    @classmethod
    def events_dict_from_line(cls, line):
        ts_values = zip(line["x"], line["y"])
        events_dict = {}
        for ts_value in ts_values:
            timestamp, value = ts_value
            events_dict[timestamp] = value

        return events_dict

    @classmethod
    def merge_new_events_dict(cls, old_events_dict, new_events_dict, event_name):
        for ts, value in new_events_dict.iteritems():
            old_events_dict[ts][event_name] = value

        return old_events_dict

    @classmethod
    def events_list_from_dict(cls, events_dict):
        events_list = []
        for ts in sorted(events_dict.keys()):
            dict_to_add = events_dict[ts]
            dict_to_add["start_iso"] = arrow.get(ts).isoformat(" ")
            events_list.append(dict_to_add)

        return events_list


class Keenio():

    def __init__(self, queries, shared_params={}):

        default_params = {
            "timeframe": "this_30_days",
            "interval": "daily",
            "timezone": 0,
        }
        url_roots = {
            "context" : "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries", 
            "production": "https://api.keen.io/3.0/projects/51d858213843314922000002/queries"
        }
        api_keys = {
            "context" : "b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e",
            "production": "69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba"
        }

        self.queries = queries
        for query in self.queries:
            #set in priority order, highest priority last
            self.queries[query]["params"] = dict(default_params.items() + shared_params.items() + queries[query]["params"].items())
            #print self.queries[query]["params"]

        for query in self.queries:
            self.queries[query]["url"] = url_roots[self.queries[query]["project"]]
            self.queries[query]["url"] += "/" + self.queries[query]["analysis"]
            self.queries[query]["url"] += "?api_key=" + api_keys[self.queries[query]["project"]]
            self.queries[query]["url"] += "&" + urllib.urlencode(self.queries[query]["params"])
            print self.queries[query]["url"]

        self.timebins = defaultdict(dict)

    def timebin_extraction_data(self, raw_data):
        pans = Widget.get_time_pan_list(100)

        for row_from_keen in raw_data:
            iso_time = row_from_keen["keen"]["timestamp"]
            time = arrow.get(str(iso_time), 'YYYY-MM-DDTHH:mm:ss')
            for key in row_from_keen.keys():
                if key not in ["keen", "userId"]:
                    pans.stomp_to_pan(time, key, row_from_keen[key])

        return pans.replace_NAs_with_zeroes().as_list()


    def get_raw_data(self, return_raw_response=False):
        response = []
        for query_name in self.queries:
            print "sending a query to keenio: " + query_name
            r = requests.get(self.queries[query_name]["url"])
            #print r.text

            raw_data = r.json()["result"]
            if return_raw_response:
                return self.get_raw_raw_data_dict()


            if self.queries[query_name]["analysis"] == "extraction":
                response = self.timebin_extraction_data(raw_data)

            else:
                for row_from_keen in raw_data:
                    new_row = self.create_row(row_from_keen, query_name)
                    self.timebins[new_row["start_iso"]].update(new_row)

        if not response:
            response = self.timebins_as_list()
        return response

    def get_raw_raw_data_dict(self):
        response = {}
        for query_name in self.queries:
            print "sending a query to keenio: " + query_name
            r = requests.get(self.queries[query_name]["url"])

            raw_data = r.json()["result"]
            response[query_name] = raw_data

        return response


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

    @classmethod
    def ungroup(cls, rows, dict_key, group_by, prepend_group_name=False):
        for row in rows:
            for groupDict in row[dict_key]:
                key = groupDict[group_by]
                if prepend_group_name:
                    key = group_by + "_" + str(key)
                val = groupDict["result"]
                row[key] = val
            del row[dict_key]
        return rows



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
    def get_ticket_stats(cls):
        logger.info("Getting uservoice ticket stats")

        owner = cls.get_uservoice_owner()

        api_response = owner.get("/api/v1/reports/agent_backlog.json")

        interesting_fields = [
            "without_response_count", 
            "waiting_for_agent_count", 
            "total_count",
            "median_open_time"
            ]

        ticket_dict = defaultdict(int)
        median_open_days = []
        for agent in api_response["entries"]:
            for field in interesting_fields:
                if field == "median_open_time":
                    median_open_days += [open_time/(60.0*60*24) for open_time in agent["open_times"]]
                else:
                    ticket_dict[field] += agent[field]


        median_open_days.sort()
        try:
            median_days = median_open_days[int(len(median_open_days)/2)]
            ticket_dict["median_open_days"] = round(median_days, 1)
        except IndexError:
            ticket_dict["median_open_days"] = 0

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
        logger.info("Getting uservoice open suggestion count")

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

    @classmethod
    def get_closed_suggestion_count(cls):
        logger.info("Getting uservoice closed suggestion count")

        owner = cls.get_uservoice_owner()

        closed_suggestions = owner.get("/api/v1/suggestions?filter=closed&per_page=1000")["suggestions"]

        logger.info("Found uservoice suggestions: {total} total".format(
            total=len(closed_suggestions)))

        return(closed_suggestions)


    @classmethod
    def get_suggestion_details(cls):
        logger.info("Getting uservoice suggestion details")

        owner = cls.get_uservoice_owner()
        suggestions_active = owner.get("/api/v1/suggestions?filter=active&per_page=1000")["suggestions"]
        suggestions_inbox = owner.get("/api/v1/suggestions?filter=inbox&per_page=1000")["suggestions"]
        suggestions = suggestions_active + suggestions_inbox

        return suggestions


class Couchdb():

    @classmethod
    def get_view(cls, full_view_name, reduce_state=False):
        logger.info("getting view from couch")

        (design_doc_name, view_name) = full_view_name.split("/")

        logger.info("full_view_name: " + full_view_name)

        if reduce_state:
            couch_query = "_design/{design_doc_name}/_view/{view_name}?reduce=true&group=true".format(
                design_doc_name=design_doc_name,
                view_name=view_name)
        else:
            couch_query = "_design/{design_doc_name}/_view/{view_name}".format(
                design_doc_name=design_doc_name,
                view_name=view_name)

        logger.info("couch_querycouch_query: " + couch_query)

        url = "/".join([
            os.getenv("CLOUDANT_URL"),
            os.getenv("CLOUDANT_DB"),
            couch_query
        ])

        logger.info("couchdb url: " + url)
        response = requests.get(url).json()

        return response["rows"]



       
