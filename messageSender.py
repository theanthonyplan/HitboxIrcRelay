# messageSender
# hitboxBridge
# 4:36 AM
#
import hitboxRelay
import json

class Sender(object):
    def __init__(self, client, user='KuoushiRelay'):
        self.client = client
        self.user = user
        self.token = None

    def login(self):
        #f = open('token', 'r')      # open the token file
        #self.token = f.read()       # save the token to self

        print self.user, self.token

        print "Attempting to join channel: kuoushi"

        data ={
            "name": "message",
            "args":[
                {
                'method': 'joinChannel',
                'params': {
                    "channel":"kuoushi",
                    "name": self.user,
                    "token": self.token
                    }
                }
            ]
        }

        msg = ('5:::'+json.dumps(data))
        print "<< Msg Sent: {}".format(data)

        self.client.sendMessage(msg, isBinary=False)

    def send(self, text):

        data ={
            "name": "message",
            "args":[
                {
                'method': 'chatMsg',
                'params': {
                    "channel":"kuoushi",
                    "name": self.user,
                    "nameColor": "FA58F4",
                    "text": text,
                    }
                }
            ]
        }

        msg = ('5:::'+json.dumps(data))

        self.client.sendMessage(msg, isBinary=False)


    def saveToken(self, t):
        self.token = t