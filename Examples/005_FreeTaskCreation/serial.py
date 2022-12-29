import __helper as h, __params as p
import time; startTimeStamp = time.time()


# create output folder
outputPath = h.prepareFolder('Output')

# load simulation parameters from params
sampleSize, poltEveryNthIteration, maxIteration = p.sampleSize, p.poltEveryNthIteration, p.maxIteration
# initialize values of x
h.Xs = [i / sampleSize for i in range(sampleSize)]
# variable for iteration number
iteration = 0

# while the simulation is not finished
while iteration <= maxIteration:

    # plot all x after every fixed number of iterations
    if iteration % poltEveryNthIteration == 0:
        h.plot(h.Xs.copy(), iteration, outputPath)

    # update the values of x
    h.iterate()
    iteration += 1

# collect all the plots and summarise as one html page
h.collectPlots(maxIteration, poltEveryNthIteration, outputPath)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
