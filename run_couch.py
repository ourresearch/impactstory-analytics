#!/usr/bin/env python

import os
import analytics
import logging


import impactstoryanalytics.widgets
from impactstoryanalytics.widgets.widget_api_helpers import Couchdb


logger = logging.getLogger("analytics.run_couch")


def run_couch():

    analytics.identify(user_id="stats")

    rows = Couchdb.get_view("collections_per_genre/collections_per_genre", True)
    products_per_quasigenre = {}
    for row in rows:
        products_per_quasigenre[row["key"]] = row["value"]

    products_per_quasigenre["total"] = products_per_quasigenre[":"]
    del products_per_quasigenre[":"]

    print products_per_quasigenre

    analytics.track(user_id="stats", event='Profiles per quasigenre', properties=products_per_quasigenre)

    return(rows)

run_couch()

#analytics.flush(async=False)  # make sure all the data gets sent to segment.io
