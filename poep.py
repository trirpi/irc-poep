import random
import settings

from password import password
import controllers.message

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol


class Poep(irc.IRCClient):
    """A fun messaging IRC bot."""

    nickname = settings.nickname

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print("[*] info: connection made")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print("[*] info: connection lost")

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)
        print("[*] info: successfully signed on to server")
        self.msg('nickserv', 'identify ' + password)
        print("[*] info: requested nick " + settings.nickname)

    def userJoined(self, user, channel):
        """Called when user joins a channel"""
        greetings = ["faka %s", "jow %s", "%s: join the club makker", "hadieho %s", "hola %s"]
        self.msg(channel, random.choice(greetings) % user)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            print("[*] info: received a private message: " + msg)
            msg = "Wat zit je nu weer te ratelen. Gooi het in de groep!"
            self.msg(user, msg)

        # Otherwise check to see if it is a message directed at me
        elif msg.startswith(settings.control_char) or msg.endswith(settings.nickname):
            if user not in settings.banned:

                # look for control_char or nick and remove it from the message
                if msg[0] == settings.control_char:
                    msg = msg[1:]
                elif msg[-5:] == " " + settings.nickname:
                    msg = msg[:-5]

                command = msg.split()[0]  # filter command from message
                try:
                    arg = msg.split(' ', 1)[1]  # the stuff after the command
                except IndexError:
                    arg = ''

                response = controllers.message.handle_message(command, arg, user)
                if response is not None:
                    self.msg(channel, response)


class LogBotFactory(protocol.ClientFactory):
    """
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = Poep()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        print("[*] warning: disconnected from server")
        print("[*] info: trying to reconnect")
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("[*] info: connection failed: ", reason)
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    f = LogBotFactory(settings.channel)
    # connect factory to this host and port
    reactor.connectTCP(settings.server, settings.port, f)
    # run bot
    print("[*] info: bot running")
    reactor.run()
