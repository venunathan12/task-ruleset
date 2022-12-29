import __helper as h, __params as p
import time; startTimeStamp = time.time()


# import required DB Module
import sqlite3
# use DB Module to get DB connection
DBConnection = h.getDBConnection(sqlite3)
# initialize the DB
h.initializeDB(DBConnection)

# for each number in params
for num in p.numsToCheckForBeingPrime:
    
    # check if the number is prime
    numIsPrime = h.isNumberPrime(num)

    # if number is prime then insert it into table
    if numIsPrime:
        h.insertNumber(DBConnection, num)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
