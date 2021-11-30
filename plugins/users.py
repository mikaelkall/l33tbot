from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyaib.plugins import msg_parser, keyword, plugin_class

@plugin_class
class UsersOnline(object):

    def __init__(self, irc_context, config):
	UsersOnline.done = False
	UsersOnline.nickPrefixes = ""
	UsersOnline.users = []

	print("Users plugin loaded, pewpew")
        self.folder = '/home/bot/bot'

    def save_users(self):
        try:
            with open("%s/users.txt" % self.folder, "w") as fp:
                for x in UsersOnline.users:
                    print("%s" % x, file=fp, end=' ')
                fp.close()
        except:
            print("Failed to dump users.txt :(")

    # Protocols from server, for prefix
    @msg_parser('005')
    def users_protocols(self, msg, irc_c):
        tmp = msg.args.split()
	for x in tmp:
            if "PREFIX" in x:
                prefix = x.split(")")
		UsersOnline.nickPrefixes = prefix[1]+":"
		print("Chanmodes prefixes set to %s" % UsersOnline.nickPrefixes)


    # Names on channel
    @msg_parser('353')
    def users_names(self, msg, irc_c):
        if UsersOnline.done == True:
            UsersOnline.done = False
            UsersOnline.users = []

	tmp = msg.args.split()
	tmp.pop(0) # Remove my nickname
	tmp.pop(0) # Remove channel privacy flag
	chan = tmp.pop(0) # Remove channel
        for x in tmp:
            while x[0] in UsersOnline.nickPrefixes:
                x = x[1:]
            UsersOnline.users.append(x)

    # End of names
    @msg_parser('366')
    def users_names_done(self, msg, irc_c):
        UsersOnline.done = True
	self.save_users()
