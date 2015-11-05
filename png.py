#! /usr/bin/python3

import pernittengryn

weblog =  pernittengryn.Log( [ {'name': 'postfix', 'search': 'relay'}, 
    {'name': 'dovecot', 'search': 'lmtp'}, {'name': 'nginx'} ] )
weblog.mail()

