#!/usr/bin/env python

# Icinga2 'High Availibity' Healthcheck
# Ugur Engin

import sys, MySQLdb
from socket import *

serverPort = 8008
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print 'HTTP server is running on port ' + str(serverPort)
while True:
    db = MySQLdb.connect("localhost","<user>","<pass>","dbname")

    cursor = db.cursor()

    q = "select NOW() - (select status_update_time from icinga_programstatus);"
    t = 60

    cursor.execute(q)
    result = cursor.fetchall()

    for date in result:
        t_out = date[0]

        cursor.close()
        db.close()

    try:
       connectionSocket, addr = serverSocket.accept()
       if (t_out <= t):
        suc_msg = "Backend" + ' ' + 'Active:' + ' ' + 'last_ts_update_seconds_ago' + ' ' + str(t_out) + '\n'
        response_body_raw = suc_msg
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'

        response_headers = {
            'Content-Type': 'text/plain',
            'Content-Length': len(response_body_raw),
        }

        response_headers_raw = ''.join('%s: %s\r\n' % (j_a, j_b)
            for j_a, j_b in response_headers.iteritems())

        connectionSocket.send('%s %s %s\r\n' % (response_proto, response_status, response_status_text))
        connectionSocket.send(response_headers_raw)
        connectionSocket.send('\r\n')
        connectionSocket.send(response_body_raw)

       else:
        response_proto = 'HTTP/1.1'
        response_status = '500'
        response_status_text = 'Internal Server Error'

        connectionSocket.send('%s %s %s' % (response_proto, response_status, response_status_text))
        connectionSocket.send('\r\n')
        connectionSocket.send('Connection: close\n')
        connectionSocket.send('\r\n')
        connectionSocket.send('<h1>500 Internal Server Error</h1>')

        connectionSocket.close()

    except OSError as e:
        sys.exit(e)
