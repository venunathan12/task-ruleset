import task_ruleset as trs
import __helper as h
import time; startTimeStamp = time.time()


# The Generator which states how tasks of type 'init' need to be performed
# It yields when a new task is ready to start execution
def rule_init(TaskKey, TaskData):

    # create output folder
    outputPath = h.prepareOutputFolder()
    # record output path in a location accessible by all processes
    trs.CommonDict['OUTPUT_PATH'] = outputPath

    # get list of input files
    inputFiles = h.getListOfFilesToProcess()

    # for each input file
    for i, fileName in enumerate(inputFiles):
        
        # create new task of type 'proc', pass name of file to process as a param
        yield trs.Task("proc", f"proc_{i}", [fileName])

    # mark this task as completed
    return


# The Function which states how tasks of type 'proc' need to be performed
# It returns an empty list since it does not schedule more tasks
def rule_proc(TaskKey, TaskData):

    # get the name of the file to process, from the params passed when creating the task
    fileName = TaskData[0]
    # get the output path recorded during execution of the initial task
    outputPath = trs.CommonDict['OUTPUT_PATH']
    
    # get data from processing the file
    processedData = h.processFile(fileName)
    
    # save data from processing
    h.saveOutputFile(outputPath, fileName.replace('.txt', ''), processedData)

    # mark this task as completed
    return []


# Details about task organisation
trs.NGuests = 4                                 # State that the tasks need to be performed on 4 processes
trs.Rules["init"] = (0, rule_init)              # Declare that there is a task of type 'init' which needs 0 params
trs.Rules["proc"] = (1, rule_proc)              # Declare that there is a task of type 'proc' which needs 1 param
trs.InitTask = trs.Task("init", "init", [])     # State that initial task is of type 'init', and does not take any params

# Only the main thread should run this code
if __name__ == '__main__':
    
    # Start execution of the tasks, starting with trs.InitTask
    trs.main()
    
    # Record the number of tasks completed by each process
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

    # Record execution time
    print(f"Completed Execution in: {time.time() - startTimeStamp} secs")
