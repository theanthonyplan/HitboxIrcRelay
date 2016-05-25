# bridge.py
# hitboxBridge
# 2:32 PM
#
import sys
from time import sleep
import getpass
from hitboxRelay import HitboxProtocol, HitboxFactory, getAuth
from ircRelay import IrcBot, IrcBotFactory
from socketLocator import SocketLocator



from twisted.internet import reactor
from twisted.python import log

# Default Hitbox info
hb_default_user = 'KuoushiRelay'


# Default IRC service information
chan = 'p0rp'
irchost = 'irc.geekshed.net'
ircport = 6667


# get hitbox credentials
hb_user = raw_input("Hitbox.tv Login?  Default: KuoushiRelay\nUsername:")
if not hb_user:                         # if no user was set
    hb_user = hb_default_user           # use the default one

hb_pw =  getpass.getpass("Password: ")

# get irc info
print "Provide the hostname of IRC, default is irc.geekshed.net"
irc_network = raw_input("\n:")

if irc_network:
    irchost = irc_network

print "Which channel would you like the relay to connect to?"
irc_chan = raw_input(":#")

if irc_chan:
    chan = irc_chan.strip('#')  # strip out extra hashes
else:
	print "defaulting to #p0rp channel"

#  First off, lets find an available socket
socket_url = None                                               # create an obj for our socket url
socket_locator = SocketLocator()                                # create a socketLocator object

print "Locating Hitbox.tv websocket URL.."
for attempt in range(20):
    try:
        connection_url = socket_locator.connection_url
        socket_url = socket_locator.socket_url                  # get the socket url

    except Exception:
        print "Failed to get websocket URL.. ",                 # report failure
        print "Retrying in 2 seconds."                                        # try again
        sleep(2)                                                # but wait 5s first
    else:
        print '=' * 60
        print "Socket URL acquired!"                            # report success
        print "Url: %s" % socket_url                            # print the URL
        print '=' * 60
        break                                                   # break the for loop

else:
    print "Failed to get socket URL after 20 attempts.  Please try again."      # too many failures
    sys.exit()                                                                  # kill the program

#  Make sure the URL was actually saved and that its a string
assert socket_url is not None

print 'v' * 50
print 'v' * 50


#  Start logging
log.startLogging(sys.stdout)


#  Now we need to get an Auth Token
#  lets save it to a file called 'token.txt'
hitbox_port = 80

hitbox_url = str(connection_url)




print "Lets try and get a token\n"
token = getAuth(hb_user, hb_pw)



#  Create the factory objects
hitbox_factory = HitboxFactory(socket_url)     # for hitbox
ircfactory = IrcBotFactory('#' + chan)                      # for irc

print "Setting Token {}!".format(token)
hitbox_factory.setToken(token)

hitbox_factory.introduceBridge(ircfactory)
print "hb test:", hitbox_factory.ircFactory
print "irc test:", ircfactory.hitboxFactory


reactor.connectTCP(hitbox_url, hitbox_port, hitbox_factory )  # hook it into the reactor
reactor.connectTCP(irchost, ircport, ircfactory )







print "Connecting to websocket: {0}:{1}".format(hitbox_url,hitbox_port)


reactor.run()
