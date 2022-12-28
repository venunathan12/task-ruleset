import task_ruleset as trs
import __helper as h, __params as p
import time; startTimeStamp = time.time()


# some variables computed based on params
# this is run on all processes and its value willl be local to the process
totalNumberoOfGoogles = len(list(p.numsToGoogle))
totalNumberOfPages = totalNumberoOfGoogles // p.pageSize + (1 if totalNumberoOfGoogles % p.pageSize > 0 else 0)

# The Generator which states how tasks of type 'init' need to be performed
def rule_init(TaskKey, TaskData):

    # create temp and output folder
    tempPath = h.prepareFolder('Temp')
    outputPath = h.prepareFolder('Output')
    # record paths in a location accessible by all processes
    trs.CommonDict['TEMP_PATH'] = tempPath
    trs.CommonDict['OUTPUT_PATH'] = outputPath

    # for each number in params
    for i, num in enumerate(p.numsToGoogle):
        
        # create new task of type 'proc', pass name of file to process as a param
        yield trs.Task("proc", f"proc_{num}", [(i, num)])
    
    # if the final page is not full
    if totalNumberoOfGoogles % p.pageSize > 0:

        # create dummy parameters for the task processing the final page
        for _ in range(p.pageSize - totalNumberoOfGoogles % p.pageSize):
            yield trs.Task("page", f"page_{(totalNumberoOfGoogles - 1) // p.pageSize}", [('pageItem', -1, None)])

    # mark this task as completed
    return


# The Generator which states how tasks of type 'proc' need to be performed
def rule_proc(TaskKey, TaskData):

    # get the number to google, from the params passed when creating the task
    param1 = TaskData[0]
    numidx, num = param1
    # get the temp path recorded during execution of the initial task
    tempPath = trs.CommonDict['TEMP_PATH']
    
    # search for the number on google and get the search results
    processedData = h.googleSearchNumber(num)
    
    # save the search results to a file
    h.saveOutputFile(tempPath, num, processedData)

    # create new task of type 'page'
    # if this task is for the first number on the page, then also pass the page number as a param to the task of type 'page'
    yield trs.Task("page", f"page_{numidx // p.pageSize}", [('pageItem', numidx, num)] + ([] if numidx % p.pageSize > 0 else [('pageNum', numidx // p.pageSize)]))

    # mark this task as completed
    return

# The Function which states how tasks of type 'page' need to be performed
def rule_page(TaskKey, TaskData):
    
    # order parameters
    TaskData.sort()

    # page number will be in the last param
    pageNum = TaskData.pop()[-1]
    # collect the numbers which should be present in this page
    pageItems = [data[2] for data in TaskData if data[1] >= 0]

    # get the paths recorded during execution of the initial task
    tempPath = trs.CommonDict['TEMP_PATH']
    outputPath = trs.CommonDict['OUTPUT_PATH']

    # format this page
    processedData = h.processPage(pageItems, tempPath, pageNum + 1, True if pageNum > 0 else False, True if pageNum + 1 < totalNumberOfPages else False)

    # save formatted page to a file
    h.saveOutputFile(outputPath, 'Page ' + str(pageNum + 1), processedData)

    # mark this task as completed
    return []


# Details about task organisation
trs.NGuests = 4                                 # State that the tasks need to be performed on 4 processes
trs.Rules["init"] = (0, rule_init)              # Declare that there is a task of type 'init' which needs 0 params
trs.Rules["proc"] = (1, rule_proc)              # Declare that there is a task of type 'proc' which needs 1 param
trs.Rules["page"] = (p.pageSize + 1, rule_page) # Declare that there is a task of type 'page' which needs 1 param for the page number and p.pageSize params for each number in the page
trs.InitTask = trs.Task("init", "init", [])     # State that initial task is of type 'init', and does not take any params

# Only the main thread should run this code
if __name__ == '__main__':
    
    # Start execution of the tasks, starting with trs.InitTask
    trs.main()
    
    # Record the number of tasks completed by each process
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

    # Record execution time
    print(f"Completed Execution in: {time.time() - startTimeStamp} secs")
