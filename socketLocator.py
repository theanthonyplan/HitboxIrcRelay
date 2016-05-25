# wsClient
# hitboxBridge
# 7:52 PM
#
from time import sleep
import urllib2 as browser

import json







class SocketLocator(object):
    def __init__(self):
        self.server_index = 0               # server index, if connection fails it will increment
        self.status = None
        self.server_list = None             # a list of dicts - key: url
        self.active_socket = None           # the active websocket
        self.auth_token = None              # acquired by logging into hitbox
        self.socket_url = None
        self.connection_url = None
        self.start()

    def start(self):
        self.status = 'ready'
        dead = -1

        print "preparing to locate socket..."

        for attempt in range(20):
            print "attempt #{0}".format(int(self.server_index) + 1)

            try:
                self.getServers()                         # get the server list
            except Exception:
                print "socket acquisition failed. retrying"
                self.server_index += 1
                sleep(.3)
            else:
                print "socket successfully located!"
                self.status = 'ok'
                break
        else:
            print 'socket acquisition failed.'

        self.getSocketUrl()



    def getServers(self, url='http://api.hitbox.tv/chat/servers?redis=true'):
        response = browser.urlopen(url)                 # request url, get a response
        html_string = response.read()                   # read the response into a string


        dict_list = json.loads(html_string)             # convert the string into a list (of dictionaries)
        server_list = []                                # a list of url strings

        for item in dict_list:                          # for each dict in the list
            for key in item:                            # and for each key in that dict
                server_list.append(item[key])           # use that key to append the url to a list

        print "Hitbox WebSocket Server URLs Acquired:"
        print '-' * 30

        for server in server_list:
            print server

        print '-' * 30

        self.server_list = server_list                              # return the list of servers


    def getSocketUrl(self):
        server_index = self.server_index
        servers = self.server_list
        websocket = None

        url_head = 'http://'                         # url prepend
        url_tail = '/socket.io/1/'                   # url append
        url_server = servers[server_index]           # get the server uri

        url = url_head + url_server + url_tail       # build the actual url

        response = browser.urlopen(url)              # request a connection Id
        connection_id = response.read()              # parse the response for the Id
        connection_id = connection_id.split(':')[0]  # get the string up until the first ':'


        wsurl = 'ws' +url[4:] + 'websocket/' + connection_id

        #print "websocket request url: {0}".format(url)

        self.socket_url = wsurl
        self.connection_url = url[7:].split('/')[0]

        print "Server URL: {0}".format(self.connection_url)
        print "Socket URL: {0}".format(self.socket_url)























