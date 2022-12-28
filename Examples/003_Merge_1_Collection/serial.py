import __helper as h, __params as p
import time; startTimeStamp = time.time()


# create output folder
tempPath = h.prepareFolder('Temp')
outputPath = h.prepareFolder('Output')

# for each number in params
for num in p.numsToGoogle:
    
    # search for the number on google and get the search results
    processedData = h.googleSearchNumber(num)
    
    # save the search results to a file
    h.saveOutputFile(tempPath, num, processedData)

# prepare the list of numbers which should be mentioned on each page
pages = []
allNumsList = list(reversed(list(p.numsToGoogle)))
while len(allNumsList) > 0:
    page = []
    for _ in range(p.pageSize):
        if len(allNumsList) > 0:
            page.append(allNumsList.pop())
    
    # variable page contains the list of numbers which should be mentioned on this page
    pages.append(page)

# for each page
for i, page in enumerate(pages):

    # format this page
    processedData = h.processPage(page, tempPath, i + 1, True if i > 0 else False, True if i + 1 < len(pages) else False)

    # save formatted page to a file
    h.saveOutputFile(outputPath, 'Page ' + str(i + 1), processedData)

# Record execution time
print(f"\n\nCompleted Execution in: {time.time() - startTimeStamp} secs")
