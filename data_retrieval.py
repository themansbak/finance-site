#!/usr/bin/python

"""
Intended for moving/storing transaction csv into database

Alex Man
"""

import os
import sys
from pprint import pprint


if len(sys.argv) < 2:
	print("python data_retrieval.py [csv-file]")
	exit()


with open(sys.argv[1], 'r') as infile:
	contents = infile.read()
	print(contents)