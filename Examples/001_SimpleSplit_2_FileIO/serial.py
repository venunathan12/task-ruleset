import __helper as h
import time; startTimeStamp = time.time()


# create output folder
outputPath = h.prepareOutputFolder()

# get list of input files
inputFiles = h.getListOfFilesToProcess()

# for each input file
for fileName in inputFiles:
    
    # get data from processing the file
    processedData = h.processFile(fileName)
    
    # save data from processing
    h.saveOutputFile(outputPath, fileName.replace('.txt', ''), processedData)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
