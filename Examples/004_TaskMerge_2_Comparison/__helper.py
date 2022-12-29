import os, sys, time
import pathlib, http.client


# Method 1 for solving DE
def solveDE_method1(xInit, timeStep, finalTime, acceleration, nextTimeInstant):

    xForEachT = []
    # Initialize time and the position and velocity of the particle
    t, x, v = 0, xInit, 0

    while t <= finalTime:

        # METHOD 1: At every instant of time, update the position and velocity of the particle
        # The new position and velocity are computed solely based on the data at the previous time instant
        x, v = x + timeStep * v, v + timeStep * acceleration(x, t)
        
        # Record the position of the particle at this instant
        xForEachT.append((t, x))
        t = nextTimeInstant(t)

    # return the complete record of the particle's position at all time
    return xForEachT


# Method 2 for solving DE
def solveDE_method2(xInit, timeStep, finalTime, acceleration, nextTimeInstant):

    xForEachT = []
    # Initialize time and the position and velocity of the particle
    t, x, v = 0, xInit, 0

    while t <= finalTime:

        # METHOD 2: At every instant of time, update the position of the particle
        # Then use the new position to compute acceleration for updating the velocity
        x = x + timeStep * v
        v = v + timeStep * acceleration(x, t)
        
        # Record the position of the particle at this instant
        xForEachT.append((t, x))
        t = nextTimeInstant(t)

    # return the complete record of the particle's position at all time
    return xForEachT


# Function to summarize the solution of a DE
def getSummaryOfSolution(solution):
    
    details = {}
    # Collect some details about the solution
    details['MIN'] = min([d[1] for d in solution])  # Collect the minimum value x over all time
    details['MAX'] = max([d[1] for d in solution])  # Collect the maximum value x over all time

    return details


# Function to compare the solutions of DE produced using different methods 
def compareResults(summary1, summary2):

    print('Using method 1:')                # Displaying results of method 1
    print(f"Minimum value of x: {summary1['MIN']}")
    print(f"Maximum value of x: {summary1['MAX']}")
    print()
    print('Using method 2:')                # Displaying results of method 2
    print(f"Minimum value of x: {summary2['MIN']}")
    print(f"Maximum value of x: {summary2['MAX']}")
    print()
    # Comparing range of x in the two solutions
    print(f"x varies in a wider range when solving the DE using method {1 if summary1['MAX'] - summary1['MIN'] > summary2['MAX'] - summary2['MIN'] else 2}")
    print()
    print()
    print()
