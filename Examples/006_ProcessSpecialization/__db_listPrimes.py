import __helper as h
import sqlite3

# connect to db
DBConnection = h.getDBConnection(sqlite3)
# get the total number of primes in the DB, and 8 of the primes
primes, count = h.getPrimes(DBConnection, 8)

# display the results
print(f"Total of {count} Prime Numbers are recorded in the DB.")
print("Some of the Prime numbers recorded in the DB are:")
print(primes)
