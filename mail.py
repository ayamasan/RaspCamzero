#! /usr/bin/python2.7
# coding: utf-8

import gmail
import os

username = 'XXX@gmail.com'
password = 'YYYYYY'

client = gmail.GMail(username, password)

body_html = u"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Face Detected.</title>
  </head>
  <body>
    <h1>picam test</h1>
  </body>
</html>
"""

message = gmail.Message(u'ZeroW', to=username, html=body_html, attachments=['zerow.jpg'])
client.send(message)
client.close()

