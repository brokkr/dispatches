#! /usr/bin/python3

import dispatches

weblog =  dispatches.Log( [ {'name': 'postfix', 'search': 'relay'}, 
    {'name': 'dovecot', 'search': 'lmtp'}, {'name': 'nginx'} ] )
weblog.mail()

