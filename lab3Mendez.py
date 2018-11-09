#Brandon Mendez
#Lab 3
#Date 10/22/2018
#Due 11/5/2018

# Create an SQL table using data read from keyboard
from urllib.request import urlopen
import sqlite3
import sys

#reads/gets the currency exchange rates
target_currency = input("Enter target currency: ")
url = "http://facweb.cdm.depaul.edu/sjost/it212/rates.txt"
response = urlopen(url)
line = str(response.read( ))

# Attach to database 
conn = sqlite3.connect('transactions.db')
cur = conn.cursor( )

# Create transactions table.
cur.execute( \
'''create table if not exists transactions(
       name varchar(15),
       date varchar(8),
       target_currency varchar(3),
       source_amount float,
       exchange_rate float,
       target_amount float
       );''' )

# Read data from keyboard.
name = input("Enter name: ")
date = input("Enter the date (00/00/00): ")
source_currency = "USD" #always in US dollar
source_amount = int(input("Enter source amount: "))

#Interpret exchange rate data from from URL
items = line.split(";")
exchange_rate = 0.0
for item in items:
    fields = item.split(",")
    code = fields[0].strip( )
    rate = float(fields[1].strip( ))
    if target_currency == code:
        exchange_rate = rate
        break;
    
if exchange_rate == 0.0:
    print("Currency not on website.")
    sys.exit( )

target_amount = source_amount * exchange_rate 
print("Target amount: " + str(target_amount))
         
# Insert values into database.
cur.execute(f'''insert into transactions values(
  '{name}','{date}','{target_currency}',{source_amount},{exchange_rate},{target_amount});''')

# Commit changes.
conn.commit( )

# Query transactions table.
cur.execute("select * from transactions;")

# Print results from query
print(cur.fetchall( ))

# Close database.
conn.close( )
