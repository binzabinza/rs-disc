#!/usr/bin/env python

import os
import sys
from importlib import import_module

sys.path.append(os.path.expanduser("~/Library/Application Support/ptpython/"))

config = import_module("config")

from models import *
import db_manager as db
from datetime import datetime
import ptpython.repl as pt


history = os.path.expanduser("~/Library/Application Support/ptpython/history")
sys.exit(pt.embed(globals(), locals(), configure=config.configure, history_filename=history))

