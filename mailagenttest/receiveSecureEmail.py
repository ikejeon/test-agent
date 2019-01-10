#!/usr/bin/env python

# '''A SSI agent that interacts by email.'''

import logging
import os
import sys
import time
import json
import datetime
import asyncio

from .mail_transport import *

def handle_msg(wc):
    # Record when we received this message.
    wc.in_time = datetime.datetime.utcnow()
    handled = False
    # decrypt wc.msg
    loop = asyncio.get_event_loop()
    # wc.obj = json.loads(wc.msg)
    return wc.msg

def fetch_msg(trans, svr, ssl, username, password, their_email):
    return trans.receive(svr, ssl, username, password, their_email)

def run(svr, ssl, username, password, their_email):
    incoming_email = None
    transport = None
    if not transport:
        transport = MailTransport()
    trans = transport
    logging.info('Agent started.')
    try:
        # while True:
        ###
        wc = fetch_msg(trans, svr, ssl, username, password, their_email)
        ###
        if wc:
            incoming_email = handle_msg(wc)
        else:
            time.sleep(2.0)
    except:
        logging.info('Agent stopped.')
    return incoming_email
