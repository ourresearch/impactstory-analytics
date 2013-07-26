#!/usr/bin/env python

import os
import analytics
import logging


import impactstoryanalytics.widgets
from impactstoryanalytics.widgets.widget_api_helpers import Couchdb


logger = logging.getLogger("analytics.run_couch")


def run_couch():

    analytics.identify(user_id="couchdb")

    rows = Couchdb.get_view("collections_per_genre/collections_per_genre", True)
    products_per_pseudogenre = {}
    for row in rows:
        products_per_pseudogenre[row["key"]] = row["value"]

    products_per_pseudogenre["total"] = products_per_pseudogenre[":"]
    del products_per_pseudogenre[":"]

    print products_per_pseudogenre

    analytics.track(user_id="couchdb", event='Profiles per pseudogenre', properties=products_per_pseudogenre)

    return(rows)

run_couch()

#analytics.flush(async=False)  # make sure all the data gets sent to segment.io
