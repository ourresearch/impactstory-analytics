#!/usr/bin/env python

import os
import analytics
import logging
import uservoice
import impactstoryanalytics


logger = logging.getLogger("analytics.uservoice_check")


def get_uservoice_owner():
    SUBDOMAIN_NAME = 'impactstory'
    API_KEY = os.getenv("USERVOICE_API_KEY")
    API_SECRET = os.getenv("USERVOICE_API_SECRET")

    client = uservoice.Client(SUBDOMAIN_NAME, API_KEY, API_SECRET)
    owner = client.login_as_owner()
    return owner

def get_ticket_counts():
    logger.info("Getting uservoice ticket count")

    owner = get_uservoice_owner()
    tickets = owner.get("/api/v1/tickets?state=open&per_page=100")["tickets"]

    last_response_was_an_admin = []
    for ticket in tickets:
        last_thread_update = max([message["updated_at"] for message in ticket["messages"]])
        last_message = [message for message in ticket["messages"] if message["updated_at"]==last_thread_update]
        last_response_was_an_admin.append(last_message[0]["is_admin_response"])

    ticket_dict = {
        "num_all_tickets": len(last_response_was_an_admin),
        "num_last_response_was_an_admin": sum(last_response_was_an_admin)
        }

    ticket_dict["num_last_response_was_a_user"] = ticket_dict["num_all_tickets"] - ticket_dict["num_last_response_was_an_admin"]

    logger.info("Found uservoice tickets: {all} total, {user} where a user answered last".format(
        all=ticket_dict["num_all_tickets"], 
        user=ticket_dict["num_last_response_was_a_user"]))

    return ticket_dict


def get_suggestion_counts():
    logger.info("Getting uservoice suggestion count")

    owner = get_uservoice_owner()
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


