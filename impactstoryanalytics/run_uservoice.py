#!/usr/bin/env python

import os
import analytics
import logging

import impactstoryanalytics.widgets
from impactstoryanalytics.widgets.widget_api_helpers import Uservoice


logger = logging.getLogger("analytics.run_uservoice")


def run_uservoice():

    analytics.identify(user_id="uservoice")

    ticket_dict = Uservoice.get_ticket_stats("Unassigned")
    print ticket_dict
    analytics.track(user_id="uservoice", event='UserVoice ticket stats', properties=ticket_dict)

    #suggestion_dict = uservoice_check.get_suggestion_counts()
    #print suggestion_dict
    #analytics.track(user_id="uservoice", event='UserVoice Suggestion check', properties=suggestion_dict)

    #return(ticket_dict, suggestion_dict)

run_uservoice()

#analytics.flush(async=False)  # make sure all the data gets sent to segment.io
