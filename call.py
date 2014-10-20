"""
call.py - Telemarketing script that displays the next name 
          and phone number of a Customer to call.

          This script is used to drive promotions for 
          specific customers based on their order history.
          We only want to call customers that have placed
          an order of over 20 Watermelons.

"""

import sqlite3

DB = None
CONN = None

# Class definition to store our customer data
class Customer(object):
	def __init__(self, id=None, first=None, last=None, telephone=None):
		## added 
		self.id = id
		self.first = first
		self.last = last
		self.telephone = telephone
		pass

	def __str__(self):
		output = "Name: %s, %s\n" % (self.last, self.first)
		output += "Phone: %s" % self.telephone

		return output

# Connect to the Database
def connect_to_db():
	global DB, CONN
	CONN = sqlite3.connect('melons.db')
	DB = CONN.cursor()


# Retrieve the next uncontacted customer record from the database.
# Return the data in a Customer class object.
#
# Remember: Our telemarketers should only be calling customers
#           who have placed orders of 20 melons or more.
def get_next_customer():
	## added in a query to select the fields from the customers and orders table with a join
	query = """SELECT customers.id, customers.givenname, customers.surname, customers.telephone
			FROM customers 
			INNER JOIN orders 
			ON customers.id = orders.customer_id
			WHERE customers.last_called IS NULL"""
	DB.execute(query)
	row = DB.fetchone()
	print row
	customer_id = row[0]
	first = row[1]
	last = row[2]
	phonenumber = row[3]
	c = Customer(customer_id, first, last, phonenumber)
	return c


def display_next_to_call(customer):
	print "---------------------"
	print "Next Customer to call"
	print "---------------------\n"
	print customer
	print "\n"


# Update the "last called" column for the customer
#   in the database.
def update_customer_called(customer):
	query = """UPDATE customers 
			SET last_called = datetime(1092941466, 'unixepoch', 'localtime')
			WHERE id=%d""" % customer.id
	DB.execute(query)
	CONN.commit()

def main():
	connect_to_db()

	done = False

	while not done:
		customer = get_next_customer()
		display_next_to_call(customer)

		print "Mark this customer as called?"
		user_answer = raw_input('(y/n) > ')

		if user_answer.lower() == 'y':
			update_customer_called(customer)
		else:
			done = True

if __name__ == '__main__':
	main()