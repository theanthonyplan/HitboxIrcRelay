# messageHandler
# hitboxBridge
# 1:49 AM
#

import json

class Handler(object):       # A class to do msg handling for a websocket
    def __init__(self, client):     # no params
        print "Message Handler Created"
        self.client = client        # save the websocket client
        self.inMsg = None           # the incoming signal
        self.outSignal = None          # the outgoing signal

    def accept(self, msg):                          # called externally to accept an incoming msg
        self.outSignal = None                       # reset the outgoing signal

        #print "|  Msg Accepted: {0}".format(msg)    # report on the inbound signal
        self.inMsg = msg                            # save the message to the handler object
        self.route(msg)                             # route the msg



    def route(self, msg):                           # call this function to handle an incoming msg
        client = self.client                        # get the websocket client
        assert client is not None                   # make sure we have a client
        assert msg == self.inMsg                    # make sure that the msg routed is what was recieved


        #print "------EVENT DETECTED-"+ '-'*20
        #print "|  onMessage() method triggered  "


                                                  #
        if msg == '1::':                                # this happens when the connection is opened
            print ">> Msg Routed:   {}".format(msg)        # confirm what msg was recieved
            print "|_ STATUS: WebSocket Connection Open"   # report the action taken

        elif msg == '2::':                                # this happens when the server pings
            print ">> Msg Routed:   {}".format(msg)          # a pong response must be sent back
            print "|_ STATUS: Pinged from WebSocket Server"  # report what it means


            self.outSignal = '2::'                        # set the outgoing signal
                                                          # encode the message

            client.sendMessage('2::')   # send the message


            print "<< Msg Sent: {}".format(self.outSignal)
            print "|_ STATUS: Pong sent to Websocket Server"


            #self.client.bridge.sendMessage('Forwarding You: %s' % msg )


        elif msg[:4] == '5:::':

            raw = msg[4:]
            z = json.loads(raw)
            b = z['args'][0]
            c = json.loads(b)
            method = c['method']

            if method == 'chatMsg':
                d = c['params']
                user = d['name']
                text = d['text']
                try:
                    m = u'[{0}]: {1}'.format(user, text).encode('ascii', 'ignore')
                except Exception:
                    print "failed to decode from unicode"

                else:
                    if user != 'KuoushiRelay':
                        self.client.factory.ircFactory.irc.forward(m)
                    #if text == '!billy':
                    #    self.client.sender.send('And they sit at the bar, and put bread in my jar.')
            #print text




        #print '-' * 41