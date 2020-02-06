#!/usr/bin/python

"""
Intended for moving/storing transaction csv into database

Alex Man
"""

from pprint import pprint
import pandas as pd
import mysql.connector
from datetime import datetime
import sys
import os
import time

read_file = True
db_debug = False

"""
Need to setup the database on new environments
"""

datafile = os.path.expanduser('~/finance-site/download.csv')

if len(sys.argv) < 2:
	print("python data_retrieval.py [csv-file]")
	exit()

print('Connecting to database')
conn = mysql.connector.connect(
	user		='root',
	password	='root',
	host		='localhost')

DB_NAME			= "transactions"
TABLE_NAME 		= "transaction"


cursor = conn.cursor()
cursor.execute('set GLOBAL max_allowed_packet=67197764')
cursor.execute('set GLOBAL net_read_timeout=60')

if not db_debug:
	try:
		statement = "create database {:s};".format(DB_NAME)
		cursor.execute(statement)
	except Exception as err:
		print('Database already exists: ', err)
	else:
		print('Created database: {:s}'.format(DB_NAME))
	
	try:
		statement = "use {:s};".format(DB_NAME)
		cursor.execute(statement)
	except Exception as err:
		print('Could not use database: ', err)
	else:
		print('Using database: {:s}'.format(DB_NAME))

	try: 
		statement = ("create table {:s} "
			"(id int auto_increment primary key, date DATE, "
			"transaction varchar(255), name longtext, memo "
			"longtext, amount int);".format(TABLE_NAME))
		cursor.execute(statement)
	except Exception as err:
		print('Could not create table: ', err)
	else:
		print('Created table')

if (read_file):
	df = pd.read_csv(datafile)
	# Date, Transaction, Name, Memo, Amount
	for index, data in df.iterrows():
		date 		= datetime.strptime(data['Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
		print(date)
		transaction = data['Transaction']
		name 		= data['Name']
		memo 		= data['Memo']
		amount 		= data['Amount']
		try:
			# statement = "insert into {} (Date) values (STR_TO_DATE(\'{}\', '%m/%d/%y'));".format(TABLE_NAME, date)
			# statement = "insert into {} (Date) values ('{}');".format(TABLE_NAME, date)
			# print(statement)
			statement = ("insert into {} (Date, Transaction, Name, Memo, Amount ",
				"values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(
					TABLE_NAME, date, transaction, name, memo, amount))
			cursor.execute(statement)
		except Exception as err:
			print('Error inserting: ', err)
			break
		time.sleep(1)

conn.close()

