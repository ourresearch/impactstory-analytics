#!/usr/bin/env python

import os
import analytics
import logging
import uservoice

import impactstoryanalytics


logger = logging.getLogger("analytics.run_uservoice")


def get_uservoice_owner():
    SUBDOMAIN_NAME = 'impactstory'
    API_KEY = os.getenv("USERVOICE_API_KEY")
    API_SECRET = os.getenv("USERVOICE_API_SECRET")

    client = uservoice.Client(SUBDOMAIN_NAME, API_KEY, API_SECRET)
    owner = client.login_as_owner()
    return owner

def check_uservoice():
    logger.info("Getting uservoice ticket count")

    owner = get_uservoice_owner()
    tickets = owner.get("/api/v1/tickets?state=open&per_page=100")["tickets"]

    last_response_was_an_admin = []
    for ticket in tickets:
        last_thread_update = max([message["updated_at"] for message in ticket["messages"]])
        last_message = [message for message in ticket["messages"] if message["updated_at"]==last_thread_update]
        last_response_was_an_admin.append(last_message[0]["is_admin_response"])

    num_all_tickets = len(last_response_was_an_admin)
    num_last_response_was_an_admin = sum(last_response_was_an_admin)
    num_last_response_was_a_user = num_all_tickets - num_last_response_was_an_admin

    logger.info("Found uservoice tickets: {all} total, {user} where a user answered last".format(
        all=num_all_tickets, 
        user=num_last_response_was_a_user))

    analytics.identify(user_id="uservoice")

    analytics.track(user_id="uservoice", event='Ticket check', properties={
        "num_all_tickets": num_all_tickets, 
        "num_last_response_was_a_user": num_last_response_was_a_user
    })

    #[suggestion["status"] for suggestion in owner.get("/api/v1/suggestions?per_page=1000")["suggestions"]]


check_uservoice()

analytics.flush(async=False)  # make sure all the data gets sent to segment.io
