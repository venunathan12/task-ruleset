import task_ruleset as trs
import __helper as h, __params as p
import time; startTimeStamp = time.time()


# The Generator which states how tasks of type 'init' need to be performed
def rule_init(TaskKey, TaskData):

    # initializing parameters of the DE
    paramsOfDE = {}
    paramsOfDE['xInit'] = p.xInit
    paramsOfDE['timeStep'] = p.timeStep
    paramsOfDE['finalTime'] = p.finalTime
    paramsOfDE['acceleration'] = p.acceleration
    paramsOfDE['nextTimeInstant'] = p.nextTimeInstant

    # create a task to solve the DE using method 1
    yield trs.Task("solve1", "solve_1", [paramsOfDE])
    # create a task to solve the DE using method 2
    yield trs.Task("solve2", "solve_2", [paramsOfDE])

    # mark this task as completed
    return


# The Generator which states how tasks of type 'solve1' need to be performed
def rule_solve1(TaskKey, TaskData):
    
    # collect params of the DE from the task's params
    paramsOfDE = TaskData[0]

    # solve DE using method 1
    xForEachT = h.solveDE_method1(**paramsOfDE)
    # collecting the summary of the solution
    summary = h.getSummaryOfSolution(xForEachT)

    # submit summary of this solution to task comp
    yield trs.Task("comp", "comp", [(TaskKey, summary)])
    
    # mark this task as completed
    return


# The Generator which states how tasks of type 'solve2' need to be performed
def rule_solve2(TaskKey, TaskData):   

    # collect params of the DE from the task's params
    paramsOfDE = TaskData[0]

    # solve DE using method 2
    xForEachT = h.solveDE_method2(**paramsOfDE)
    # collecting the summary of the solution
    summary = h.getSummaryOfSolution(xForEachT)

    # submit summary of this solution to task comp
    yield trs.Task("comp", "comp", [(TaskKey, summary)])

    # mark this task as completed
    return


# The Function which states how tasks of type 'comp' need to be performed
def rule_comp(TaskKey, TaskData):
    
    # order the task's params
    TaskData.sort()
    # collect the 2 summaries submitted by task solve1 and solve2
    summary_method1, summary_method2 = [item[1] for item in TaskData]

    # comparing results
    h.compareResults(summary_method1, summary_method2)

    # mark this task as completed
    return []


# Details about task organisation
trs.NGuests = 2                                 # State that the tasks need to be performed on 2 processes
trs.Rules["init"] = (0, rule_init)              # Declare that there is a task of type 'init' which needs 0 params
trs.Rules["solve1"] = (1, rule_solve1)          # Declare that there is a task of type 'solve1' which needs 1 param
trs.Rules["solve2"] = (1, rule_solve2)          # Declare that there is a task of type 'solve2' which needs 1 param
trs.Rules["comp"] = (2, rule_comp)              # Declare that there is a task of type 'comp' which needs 2 param
trs.InitTask = trs.Task("init", "init", [])     # State that initial task is of type 'init', and does not take any params

# Only the main thread should run this code
if __name__ == '__main__':
    
    # Start execution of the tasks, starting with trs.InitTask
    trs.main()
    
    # Record the number of tasks completed by each process
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

    # Record execution time
    print(f"Completed Execution in: {time.time() - startTimeStamp} secs")
