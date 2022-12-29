import task_ruleset as trs
import __helper as h, __params as p
import time; startTimeStamp = time.time()


# The function that should run at the creation of each process
def ProcessInit(id):
    
    # process 8 needs get DB connection and initialize the DB
    if id == 8:

        # import required DB Module
        import sqlite3
        # use DB Module to get DB connection
        trs.ProcessDict['DBConnection'] = h.getDBConnection(sqlite3)
        # initialize the DB
        h.initializeDB(trs.ProcessDict['DBConnection'])
    
    return

# State that function ProcessInit should run at the start of each process
trs.ProcessInit = ProcessInit


# The Generator which states how tasks of type 'init' need to be performed
def rule_init(TaskKey, TaskData):

    # for each number in params
    for num in p.numsToCheckForBeingPrime:
        
        # create new task of type 'check', pass number to check for primality
        yield trs.Task("check", f"check_{num}", [num])

    # mark this task as completed
    return


# The Function which states how tasks of type 'check' need to be performed
def rule_check(TaskKey, TaskData):

    # get the number to check, from the params passed when creating the task
    num = TaskData[0]
    
    # check if the number is prime
    numIsPrime = h.isNumberPrime(num)

    # if number is prime then create new task to insert the number into table
    if numIsPrime:
        yield trs.Task("insert", f"insert_{num}", [num])

    # mark this task as completed
    return


# The Function which states how tasks of type 'insert' need to be performed
def rule_insert(TaskKey, TaskData):

    # get the number to insert, from the params passed when creating the task
    num = TaskData[0]
    
    # insert the number into the table
    h.insertNumber(trs.ProcessDict['DBConnection'], num)

    # mark this task as completed
    return


# Details about task organisation
trs.NGuests = 8                                         # State that the tasks need to be performed on 8 processes
trs.Rules["init"] = (0, rule_init)                      # Declare that there is a task of type 'init' which needs 0 params
trs.Rules["check"] = (1, rule_check, range(1, 7 + 1))   # Declare that there is a task of type 'check' which needs 1 param, this task can only be run on processes 1 to 7
trs.Rules["insert"] = (1, rule_insert, [8])             # Declare that there is a task of type 'insert' which needs 1 param, this task can only be run on process 8
trs.InitTask = trs.Task("init", "init", [])             # State that initial task is of type 'init', and does not take any params

# Only the main thread should run this code
if __name__ == '__main__':
    
    # Start execution of the tasks, starting with trs.InitTask
    trs.main()
    
    # Record the number of tasks completed by each process
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

    # Record execution time
    print(f"Completed Execution in: {time.time() - startTimeStamp} secs")
