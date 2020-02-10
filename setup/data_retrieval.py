#!/usr/bin/python

"""
Intended for moving/storing transaction csv into database
Need to setup the database on new environments

Alex Man
"""

from pprint import pprint
import pandas as pd
import mysql.connector
from datetime import datetime
import sys
import os
import time
import json

read_file = False
db_debug = False


datafile = os.path.expanduser('~/finance-site/download.csv')

if len(sys.argv) < 2:
	print("python3 data_retrieval.py [csv-file]")
	exit()

print('Opening config file')
with open('config.json', 'r') as infile:
	configs = json.load(infile)
	print(configs)

print('Connecting to database')
conn = mysql.connector.connect(
	user		= configs['db_connection']['user'],
	password	= configs['db_connection']['pwd'],
	host		= configs['db_connection']['host'])


DB_NAME			= "transactions"
TABLE_NAME 		= "transaction"
LOGIN_TABLE		= "login"

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
			"longtext, amount double);".format(TABLE_NAME))
		cursor.execute(statement)
	except Exception as err:
		print('Could not create table: ', err)
	else:
		print('Created {:s} table'.format(TABLE_TABLE))

	try:
		statement = ("create table {:s} "
			"(username varchar(255), "
			"password varchar(255), "
			"salt varchar(5));".format(LOGIN_TABLE))
		cursor.execute(statement)
	except Exception as err:
		print('Could not create table: ', err)
	else:
		print('Created {:s} table'.format(LOGIN_TABLE))

if (read_file):
	df = pd.read_csv(datafile)
	# Date, Transaction, Name, Memo, Amount
	for index, data in df.iterrows():
		date 		= datetime.strptime(data['Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
		transaction = data['Transaction']
		name 		= data['Name'].replace('\'','-')
		memo 		= data['Memo']
		amount 		= data['Amount']
		try:
			statement = "insert into {} (Date, Memo, Name) values ('{}', '{}', '{}')".format(
				TABLE_NAME, date, memo, name)
			cursor.execute(statement)
			conn.commit()

			statement = "update {} set Transaction='{}', Amount='{}' where Memo='{}'".format(
				TABLE_NAME, transaction, amount, memo)
			cursor.execute(statement)
			conn.commit()
		except Exception as err:
			print('Error inserting: ', err)
			break

conn.close()

