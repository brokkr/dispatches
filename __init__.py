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
    def __init__(self, services):
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)
        timeago = datetime.now() - timedelta(days=3, minutes=10)
        j.seek_realtime(timeago)
        
        self.filtered = []
        self.raw = []
        for entry in j:
            entry['_SYSTEMD_UNIT'] = entry.get('_SYSTEMD_UNIT', None)
            self.raw.append(entry)

        for service in services:
            subset = [ x for x in self.raw if x['_SYSTEMD_UNIT'] == service['name'] ]
            print(subset)
            #slog = Slog(service, subset)
            #self.filtered.append(slog)

class Slog():
    def __init__(self, service):
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

