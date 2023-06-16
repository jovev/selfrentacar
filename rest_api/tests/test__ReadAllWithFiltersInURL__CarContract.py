#!/usr/bin/python2

import requests, json


print ('\n 1. Login in Odoo and get access tokens:')
r = requests.post(
    'http://localhost:8069/api/auth/get_tokens',
    headers = {'Content-Type': 'text/html; charset=utf-8'},
    data = json.dumps({
        'username': 'odoo@irvas.rs',
        'password': 'irvasadm',
    }),
    #verify = False      # for TLS/SSL connection
)
print (r.text)
access_token = r.json()['access_token']


print ('\n 2. res.partner - Read all (with filters in URL):')
r = requests.get(
    "http://localhost:8069/api/car.rental.contract?filters=[('state','=','reserved')]",
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Token': access_token
    },
    #verify = False      # for TLS/SSL connection
)
print (r.text)
