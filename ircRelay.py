# irc
# hitboxBridge
# 4:01 AM
#
from twisted.internet.protocol import Protocol, Factory


from twisted.words.protocols import irc
from twisted.internet import protocol

class IrcBot(irc.IRCClient):
    def __init__(self, f):
        self.factory = f
        self.admins = ['p0rp', 'kuoushi', 'pr0p']

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def bindCommands(self):
        #  To bind a command, add an entry to the self.commands tuple
        #  The tuple is of length 3 and is as follows (user, command, action)
        #  the user name must be None else it will restrict who is able to invoke that command
        #  command is the string to match and action is the function that will be called
        #  if action is a string, it will be printed to irc chat
        self.commands = [(False, '!elton', "Hold me closer, Tony Danza."),
                         (False, '!smoke', "Here bud, I've got a light."),
                         (True, '!restart', self.factory.connector.disconnect),
                         ]


    def signedOn(self):
        self.bindCommands()
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

        print "PRINTING IRC FACTORY"
        print self.factory
        print "PRINTING RELAY"


    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        print user.split('!')[0]+': '+msg
        raw_user = user.split('!')[0]
        print "RAW USER: {}".format(raw_user)
        if msg[0] == '!':                              # if the first char is "!"
            self.matchCommand(raw_user, msg)           # try to match the string
        else:
            u = user.split('!')[0]
            self.factory.hitbox.sender.send('[{0}]: {1}'.format(u, msg))

    def forward(self, m):
        self.msg(self.factory.channel, m)

    def matchCommand(self, user, msg):
        #if self.debug is True:
        #    print "Matching: {}".format(msg)

        for u,m,a in self.commands:
            print u,m,a
            if m == msg:
                print "m matched!"
                print "user: {}".format(user)
                print "user: {}".format(user)
                if type(a) == type('string'):
                    self.msg(self.factory.channel, a)
                    return u,m,a
                else:
                    if u is not False:
                        if user in self.admins:         # check if user is in admin list
                            a()




class IrcBotFactory(protocol.ClientFactory):
    def __init__(self, channel, nickname='KuoushiRelay', ):
        self.channel = channel
        self.nickname = nickname

        self.irc = None
        self.hitboxFactory = None
        self.protocol = IrcBot(self)

    def buildProtocol(self, addr):
        print 'Connected.'
        self.irc = IrcBot(self)

        self.hitbox = self.hitboxFactory.makeBridge()     # assemble the bridge

        print "^^^TESTING BRIGE^^^"
        print "TESTING HITBOX CONNECTION {}".format(self.hitbox)
        print "TESTING HITBOX CONNECTION {}".format(self.hitboxFactory.irc)

        return self.irc

    def getIrc(self):
        return self.irc

    def startedConnecting(self, connector):
        print "Saving connector to Bot Factory"
        print "connector: {}".format(connector)
        self.connector = connector

        print "Connector succesfully saved."


    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)






if __name__ == "__main__":





 #  IRC service information
    chan = 'kuoushi'
    irchost = 'irc.geekshed.net'
    ircport = 6667
    ircfactory = PorpBotFactory('#' + chan)


    print "I am about to connect to the IRC network"
    reactor.connectTCP(irchost, ircport, ircfactory )


