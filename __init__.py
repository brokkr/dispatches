#!/usr/bin/env python3

from systemd import journal
from datetime import datetime,timedelta
import re
import smtplib
from email.mime.text import MIMEText

# Open the journal for reading, set log level and go back one day and 10 minutes
class Log():
    def __init__(self):
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)
        yesterday = datetime.now() - timedelta(days=3, minutes=10)
        j.seek_realtime(yesterday)

        self.info = []

        # Filter and store output
        for entry in j:
            self.info.append(entry)


