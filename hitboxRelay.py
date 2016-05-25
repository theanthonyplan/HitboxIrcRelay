# wsClient
# hitboxBridge
# 7:52 PM
#
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from messageRouter import Handler
from messageSender import Sender

from time import sleep

import httplib
import json

#login="KuoushiRelay", pw='heresapassword'
def getAuth(login="", pw=''):


    for attempt in range(20):
        try:
            connection = httplib.HTTPSConnection(host='www.hitbox.tv')
            print '-' * 30
            print "Hitbox.tv Authentication"
            print "Getting authentication token for user: %s" % login

            data = json.dumps({"login": login, "pass": pw, "rememberme": ""})

            connection.request("POST", '/api/auth/token', data)
            response = json.loads(connection.getresponse().read())
            connection.close()

            token = response['authToken']


        except Exception:
            print "failed to get Auth token.  Retrying in 5 seconds..."
            sleep(5)

        else:
            print "Auth token successfully acquired!"
            print "Auth token: %s" % token
            print "-" * 30
            break
    else:
        print "Failed to acquire an Auth token after 20 attemps.  Please try again."



    return token



class HitboxProtocol(WebSocketClientProtocol):
    def __init__(self, f):
        print "Hitbox Protocol Initialized..."
        self.socket = None
        self.messages = list()
        self.isLoggedIn = False
        self.handler = Handler(self)
        self.sender = Sender(self)
        self.factory = f
        self.token = f.token



    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        print "Logging into hitbox.tv"




    def onOpen(self):
        print("WebSocket connection open.")


        print "PRINTING HITBOX FACTORY"
        print self.factory
        print "Saving Token!"




    def onMessage(self, payload, isBinary):
        if payload is not None:
            self.handler.accept(payload)     # accept the msg and get a response


        try:
            if self.isLoggedIn is False:
                self.sender.saveToken(self.token)
                self.sender.login()
                self.isLoggedIn = True
        except Exception:
            print "failure during login attempt"


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class HitboxFactory(WebSocketClientFactory, ReconnectingClientFactory):
    #protocol = HitboxProtocol

    def buildProtocol(self, addr):
        print 'Connected.  Creating a Hitbox Factory.'
        self.hitbox = HitboxProtocol(self)
        return self.hitbox

    def startedConnecting(self, connector):
        print "started connecting!"

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        self.irc.sender.send("Restarting Hitbox")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def getHitbox(self):
        return self.hitbox

    def setToken(self, token):
        self.token = token

    def introduceBridge(self, ircFactory):
        self.ircFactory = ircFactory
        ircFactory.hitboxFactory = self

        return ircFactory.hitboxFactory

    def makeBridge(self):
        self.irc = self.ircFactory.getIrc()            # first we need to save the irc bot
        return self.getHitbox()                    # then return our hitbox bridge relay





































