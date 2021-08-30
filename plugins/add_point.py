#!/usr/bin/env python
# Hack if want to bump someones points.
import datetime
import pickle
import time
import random
import os

score = {}
flist = []

folder = '/home/bot/bot'

try:
    score = pickle.load( open( "%s/highscore.p" % folder, "rb" ) )
except:
    score = {}

name = 'user'
score[name]
score[name] = int(score[name]) + 1

pickle.dump( score, open( "%s/highscore.p" % folder, "wb" ) )

