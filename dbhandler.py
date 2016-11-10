from mysql.connector import MySQLConnection, Error
from configparse import read_db_config
from datetime import datetime

def init():
	print ("init db")
#	global dbconfig
#	dbconfig = read_db_config()

#def insert(user, token):


def getUser(token):
	user = {}

	try:
		dbconfig = read_db_config()

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
		
