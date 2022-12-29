import __helper as h, __params as p
import time; startTimeStamp = time.time()


# initializing parameters of the DE
paramsOfDE = {}
paramsOfDE['xInit'] = p.xInit
paramsOfDE['timeStep'] = p.timeStep
paramsOfDE['finalTime'] = p.finalTime
paramsOfDE['acceleration'] = p.acceleration
paramsOfDE['nextTimeInstant'] = p.nextTimeInstant

# solve DE using method 1
xForEachT_method1 = h.solveDE_method1(**paramsOfDE)
# collecting the summary of the solution
summary_method1 = h.getSummaryOfSolution(xForEachT_method1)

# solve DE using method 2
xForEachT_method2 = h.solveDE_method2(**paramsOfDE)
# collecting the summary of the solution
summary_method2 = h.getSummaryOfSolution(xForEachT_method2)

# comparing results
h.compareResults(summary_method1, summary_method2)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
