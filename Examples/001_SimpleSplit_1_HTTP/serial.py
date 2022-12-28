import __helper as h, __params as p
import time; startTimeStamp = time.time()


# create output folder
outputPath = h.prepareOutputFolder()

# for each number in params
for num in p.numsToGoogle:
    
    # search for the number on google and get the search results
    processedData = h.googleSearchNumber(num)
    
    # save the search results to a file
    h.saveOutputFile(outputPath, num, processedData)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
