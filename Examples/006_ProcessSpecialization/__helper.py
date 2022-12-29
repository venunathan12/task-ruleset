import os, sys, time
import sqlite3


# Function to check if a number is prime
def isNumberPrime(num):
    
    isPrime = True

    i = 2
    while i * i <= num:

        if num % i == 0:
            isPrime = False

        i += 1

    return isPrime


# Function to get DB Connection
def getDBConnection(DBModule):

    connection = DBModule.connect('__DB')

    return connection


# Function to create new table in DB if it does not exist
def initializeDB(connection):
    
    cursor = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS primes
        ([number] INTEGER PRIMARY KEY)
        '''
    )

    connection.commit()

    return


# Function to query the table in the DB and get the stored primes
def getPrimes(connection, count = None):

    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT number FROM primes
        '''
    )

    primes = cursor.fetchall()
    totalCount = len(primes)
    
    if count is not None:
        primes = primes[0 : count]
    
    if len(primes) > 0:
        primes = [r[0] for r in primes]

    return primes, totalCount


# Function to insert a number into the table
def insertNumber(connection, num):

    cursor = connection.cursor()

    try:
    
        cursor.execute(
            f'''
            INSERT INTO primes
            VALUES ({num})
            '''
        )

        connection.commit()
    
    except:

        connection.rollback()

    return
