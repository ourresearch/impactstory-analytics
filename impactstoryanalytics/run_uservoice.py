#!/usr/bin/env python

import os
import analytics
import logging

from impactstoryanalytics import uservoice_check


logger = logging.getLogger("analytics.run_uservoice")


def run_uservoice():
    (num_all_tickets, num_user, num_admin) = uservoice_check.get_ticket_counts()

    logger.info("Found uservoice tickets: {all} total, {user} where a user answered last".format(
        all=num_all_tickets, 
        user=num_user))

    analytics.identify(user_id="uservoice")

    analytics.track(user_id="uservoice", event='Ticket check', properties={
        "num_all_tickets": num_all_tickets, 
        "num_last_response_was_a_user": num_user,
        "num_last_response_was_an_admin": num_admin
    })

    return(num_all_tickets, num_user, num_admin)

run_uservoice()

analytics.flush(async=False)  # make sure all the data gets sent to segment.io
