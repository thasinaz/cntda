#!/usr/bin/env python3

import sys, time, threading
from socket import *

from Heartbeater import Heartbeater

args = sys.argv
address = (sys.argv[1], int(sys.argv[2]))

Heartbeater(address).run()

sys.exit()
