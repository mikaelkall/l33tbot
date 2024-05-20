# nighter@nighter.se
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import pickle
import time
import random
import os
from pyaib.plugins import keyword, plugin_class


class Stats(object):

    def __init__(self):

        self.score = {}
        self.flist = []

        self.folder = '/home/bot/bot'

        try:
            self.score = pickle.load( open( "%s/highscore.p" % self.folder, "rb" ) )
        except:
            self.score = {}
        
        try:
            self.flist = pickle.load( open( "%s/flist.p" % self.folder, "rb") )
        except:
            self.flist = []

    def add_flist(self, name):
        self.flist.append(name)
        pickle.dump(self.flist, open("%s/flist.p" % self.folder, "wb"))

    def add_score(self, name):
        try:
            self.score[name]
        except:
            self.score[name] = 0
    
        self.score[name] = int(self.score[name]) + 1
        pickle.dump( self.score, open( "%s/highscore.p" % self.folder, "wb" ) )


    def list_score(self, msg, irc_c, luckyluke):

        if len(self.score) == 0:
            msg.reply("Empty highscore")
            return

        if os.path.isfile('%s/champ.txt' % self.folder) is True:
            with open('%s/champ.txt' % self.folder, 'r') as file:
                 try:
                     champ = file.readlines()[0].strip()
                     irc_c.PRIVMSG("%s" % (msg.nick), "LeetChamp: %s" % champ)
                 except:
                     pass

        try:
            if len(luckyluke) > 1:
                irc_c.PRIVMSG("%s" % (msg.nick), "LuckyLuke: %s" % luckyluke)
        except:
            pass

        irc_c.PRIVMSG("%s" % (msg.nick), "-----------------------------")

        for key, elem in reversed(sorted(self.score.iteritems(), key=lambda (k,v): (v,k))):
            irc_c.PRIVMSG("%s" % (msg.nick), "%s:%s" % (key, elem))
            time.sleep(1)
    


@plugin_class
class Leet(object):

    def __init__(self, irc_context, config):
        Leet.block = False
        print("L33t Plugin Loaded!")

        self.folder = '/home/bot/bot'
        self.spamuser = ''

        if os.path.isfile('%s/luckyluke.txt' % self.folder) is True:
            with open('%s/luckyluke.txt' % self.folder, 'r') as file:
                try:
                     self.luckyluke = file.readlines()[0].strip()
                except:
                    self.luckyluke = ''
        else:
            self.luckyluke = ''

    @keyword('lucky')
    @keyword.nosubs
    def lucky_root(self, irc_c, msg, trigger, args, kargs):

        if self.spamuser == msg.nick:
            msg.reply("Stop the spam: %s" % msg.nick)
            self.spamuser = msg.nick
            return

        mytime = str(datetime.datetime.now().time())
        if mytime[:3] == "13:":
            
            if os.path.isfile('%s/users.txt' % self.folder) is True:
                with open('%s/users.txt' % self.folder, 'r') as file:
                    try:
                        users = file.readlines()[0].strip().split(' ')
                    except:
                        users = ''
            else:
                users = ''
            
            random.shuffle(users)
            if users[0] == msg.nick:
                msg.reply("** You %s %s **" % (msg.nick, "are now LuckyLuke"))
                self.luckyluke = msg.nick

                with open('%s/luckyluke.txt' % self.folder, 'w') as file:
                    file.write(msg.nick)

            else:
                msg.reply("Spotlight was on %s" % users[0])
                self.spamuser = msg.nick
        else:
            msg.reply("It is not time for LuckyLuke")

    @keyword('1337')
    @keyword.nosubs
    def leet_root(self, irc_c, msg, trigger, args, kargs):
        mytime=str(datetime.datetime.now().time())
        if mytime[:5] == "13:37":

            if Leet.block == False:

                if msg.nick in Stats().flist:
                    msg.reply("Sorry %s you have already played today!" % msg.nick)
                    return

                Leet.block = True
                msg.reply("**** Congratulations %s %s (%s) ****" % (msg.nick, "you are the winner!", mytime))
                Stats().add_score(msg.nick)

                if msg.nick == self.luckyluke:
                    msg.reply("**** Congratulations %s %s (%s) ****" % (msg.nick, "you are LuckyLuke +2 extra point", mytime))
                    Stats().add_score(msg.nick)
                    Stats().add_score(msg.nick)
            else:
                msg.reply("Sorry %s %s" % (msg.nick, "we already have a winner today."))

        else:
            Leet.block = False
            msg.reply("Sorry %s %s" % (msg.nick, "Time is not 13:37! Thanks for playing!"))
            Stats().add_flist(msg.nick)


    @keyword('rules')
    @keyword.nosubs
    def rules_root(self, irc_c, msg, trigger, args, kargs):
        mytime=str(datetime.datetime.now().time())
        if mytime[:5] != "13:37":
            Leet.block = False
        msg.reply("Welcome to the 1337 game.")
        time.sleep(1)
        msg.reply("To win type !1337 at 13:37. If you are first you win!")
        time.sleep(1)
        msg.reply("Available commands")
        time.sleep(1)
        msg.reply("!rules   Show rules.")
        time.sleep(1)
        msg.reply("!1337    Try to win.")
        time.sleep(1)
        msg.reply("!lucky    Try to become LuckyLuke")
        time.sleep(1)
        msg.reply("!stats   View highscore list.") 

    @keyword('stats')
    @keyword.nosubs
    def stats_root(self, irc_c, msg, trigger, args, kargs):
        mytime=str(datetime.datetime.now().time())
        if mytime[:5] != "13:37":
            Leet.block = False
        Stats().list_score(msg, irc_c, self.luckyluke)











