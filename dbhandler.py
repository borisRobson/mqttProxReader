from mysql.connector import MySQLConnection, Error
from configparse import read_config
from datetime import datetime

def init():
	print ("init db")
#	global dbconfig
#	dbconfig = read_db_config()

def insert(user, token):
	query = "INSERT INTO Users(Name, TokenID)"\
		"VALUES(%s, %s)"
	args = (user, str(token))
#	print args
	try:
		db_config = read_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute(query, args)

		conn.commit()

	except Error as e:
		print(e)

	finally:
		print ("Added User: {0}, TokenId: {1}").format(user, token)
		cursor.close()
		conn.close()

def remove(name):
	db_config = read_config()
	
	query = "DELETE FROM Users Where Name = %s"

	try:
		conn = MySQLConnection(**db_config)
		cursor = conn.cursor()
		cursor.execute(query, (name,))

		conn.commit()

	except Error as e:
		print(e)

	finally:
		cursor.close()
		conn.close()
	
		

def getUser(token):
	user = {}

	try:
		dbconfig = read_config('config.ini', 'mysql')

		conn = MySQLConnection(**dbconfig)
		query = ("SELECT * from Users Where TokenId = {0}".format(str(token)))
		

		cursor = conn.cursor()
		cursor.execute(query)

		row = cursor.fetchone()
		while row != None:
			user = row
			row = cursor.fetchone()

	except Error as e:
		print(e)

	finally:
		cursor.close()
		conn.close()
		return user
		
