import __helper as h
import time; startTimeStamp = time.time()


# the list of numbers we wish to google
numsToPull = range(1, 64 + 1)


# create output folder
outputPath = h.prepareOutputFolder()

# for each number
for num in numsToPull:
    
    # search for the number on google and get the search results
    processedData = h.googleSearchNumber(num)
    
    # save the search results to a file
    h.saveOutputFile(outputPath, num, processedData)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
