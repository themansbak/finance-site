#!/usr/bin/python

"""
Intended for moving/storing transaction csv into database

Alex Man
"""

import pandas as pd
from pprint import pprint
import mysql.connector
import sys
import os

"""
Need to setup the database on new environments
"""

datafile = os.path.expanduser('~/finance-site/download.csv')

if len(sys.argv) < 2:
	print("python data_retrieval.py [csv-file]")
	exit()


df = pd.read_csv(datafile)
# pprint(df)

conn = mysql.connector.connect(
	user		='root',
	password	='root',
	host		='localhost')


cursor = conn.cursor()

try:
	statement = "create database transactions;"
	cursor.execute(statement)
except Exception as err:
	print('Database already exists: ', err)



conn.close()

