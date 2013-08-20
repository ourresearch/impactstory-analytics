#!/usr/bin/env python

import os
import analytics
import logging

import impactstoryanalytics.widgets
from impactstoryanalytics.widgets.widget_api_helpers import Uservoice


logger = logging.getLogger("analytics.run_uservoice")


def run_uservoice():

    analytics.identify(user_id="uservoice")

    ticket_dict = Uservoice.get_ticket_stats()
    print ticket_dict
    analytics.track(user_id="uservoice", event='UserVoice ticket stats', properties=ticket_dict)

    return(ticket_dict)

run_uservoice()

analytics.flush(async=False)  # make sure all the data gets sent to segment.io
