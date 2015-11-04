#!/usr/bin/env python3

# Copyright 2014 Timothée Ravier 
# https://tim.siosm.fr/blog/2014/02/24/journald-log-scanner-python / CC-BY-SA 4.0
# Contributions Copyright 2015 Mads Michelsen 
# https://github.com/brokkr/pernittengryn / GPLv3
# License compatibility: http://creativecommons.org/compatiblelicenses

from systemd import journal
from datetime import datetime,timedelta
import re
import smtplib
from email.mime.text import MIMEText

# Open the journal for reading, set log level and go back one day and 10 minutes
class Log():
    def __init__(self, service_name):
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)
        yesterday = datetime.now() - timedelta(days=3, minutes=10)
        j.seek_realtime(yesterday)

        self.service_name = service_name
        self.info = []

        # Filter and store output
        for entry in j:
            try:
                if entry['_SYSTEMD_UNIT'] == service_name:
                    humantime =  entry['__REALTIME_TIMESTAMP'].strftime("%Y-%m-%d %H:%M:%S")
                    service_tpl = (service_name, humantime, entry['MESSAGE'])
                    service_msg = ' | '.join(service_tpl)
                    self.info.append(service_msg)
            except KeyError:
                pass

    def mail(self):
        # Send the content in a mail to root
        mail = MIMEText('\n'.join(self.info))
        mail['Subject'] = '[THEMINT] Logs from ' + self.service_name
        mail['From'] = 'root@localhost'
        mail['To'] = 'root@localhost'
        server = smtplib.SMTP('localhost')
        server.send_message(mail)
        server.quit()

