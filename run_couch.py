#!/usr/bin/env python

import os
import analytics
import logging


import impactstoryanalytics.widgets
from impactstoryanalytics.widgets.widget_api_helpers import Couchdb


logger = logging.getLogger("analytics.run_couch")


def run_couch():

    #analytics.identify(user_id="couchdb")

    rows = Couchdb.get_view("collections_per_genre/collections_per_genre", True, True)
    for row in rows:
    	print row
    #analytics.track(user_id="uservoice", event='UserVoice ticket stats', properties=ticket_dict)

    return(rows)

run_couch()

#analytics.flush(async=False)  # make sure all the data gets sent to segment.io
