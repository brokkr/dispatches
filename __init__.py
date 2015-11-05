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
        
        self.msgstring = ''
        self.filtered = []
        self.raw = []
        for entry in j:
            entry['_SYSTEMD_UNIT'] = entry.get('_SYSTEMD_UNIT', None)
            self.raw.append(entry)

        for service in services:
            sname = service['name'] + '.service'
            subset = [ x for x in self.raw if x['_SYSTEMD_UNIT'] == sname ]
            #print(subset)
            slog = Slog(service, subset)
            self.filtered.append(slog)
            self.msgstring = self.msgstring + slog.msgstring

    def mail(self):
        # Send the content in a mail to root
        mail = MIMEText(self.msgstring)
        mail['Subject'] = '[THEMINT] Logs'
        mail['From'] = 'root@localhost'
        mail['To'] = 'root@localhost'
        server = smtplib.SMTP('localhost')
        server.send_message(mail)
        server.quit()

class Slog():
    def __init__(self, service, subset):
        self.service_name = service['name']
        errors = [ ( self.htime(x['__REALTIME_TIMESTAMP']), str(x['PRIORITY']), 
            x['MESSAGE'] ) for x in subset if x['PRIORITY'] < 4 ]
        try:
            searches = [ ( self.htime(x['__REALTIME_TIMESTAMP']), str(x['PRIORITY']), 
                x['MESSAGE']) for x in subset if service['search'] in x['MESSAGE'] ]
        except KeyError:
            searches = []
        self.errormsgs = [ ' | '.join(x) for x in errors ]
        self.searchmsgs = [ ' | '.join(x) for x in searches ]
        errorstr = '    Errors\n' + '\n        '.join(self.errormsgs)
        searchstr = '    Searches\n        ' + '\n        '.join(self.searchmsgs)
        self.msgstring = ' '.join(self.service_name).upper() + '\n' + \
           errorstr + '\n' + searchstr + '\n' 

    def htime(self, timestamp):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

