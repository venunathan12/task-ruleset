# This file contains all the specifications about the work we wish our program to do
# This file is imported both in the serial and parallel implementation of our program

# Following are the parameters for solving a differential equation
# This DE expresses the acceleration of a particle as a function of time and its current position
# The particle is assumed to be starting from rest

xInit = 1                   # Starting position of the particle
timeStep = 0.0001           # Time step while solving the DE
finalTime = 600             # The time till which we wish to compute the solution

def acceleration(x, t):     # Acceleration of the particle as a function of time and its current position
    return - 1 * x

def nextTimeInstant(t):     # Function to get the next time instant
    return round(t + timeStep, 6)
