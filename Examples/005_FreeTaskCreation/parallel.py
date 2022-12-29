import task_ruleset as trs
import __helper as h, __params as p
import time; startTimeStamp = time.time()


# The Generator which states how tasks of type 'init' need to be performed
def rule_init(TaskKey, TaskData):

    # create output folder
    outputPath = h.prepareFolder('Output')
    # record paths in a location accessible by all processes
    trs.CommonDict['OUTPUT_PATH'] = outputPath

    # create the task to run the simulation
    yield trs.Task('sim', 'sim', [(p.sampleSize, p.poltEveryNthIteration, p.maxIteration)])

    # mark this task as completed
    return


# The Generator which states how tasks of type 'sim' need to be performed
def rule_sim(TaskKey, TaskData):
    
    # load simulation parameters from task params
    simParams = TaskData[0]
    sampleSize, poltEveryNthIteration, maxIteration = simParams
    # initialize values of x
    h.Xs = [i / sampleSize for i in range(sampleSize)]
    # variable for iteration number
    iteration = 0

    # while the simulation is not finished
    while iteration <= maxIteration:

        # every fixed number of iterations, create task to plot the values of x
        if iteration % poltEveryNthIteration == 0:
            yield trs.Task('plot', f'plot_{iteration}', [(h.Xs.copy(), iteration, maxIteration, poltEveryNthIteration)])

        # update the values of x
        h.iterate()
        iteration += 1
    
    # create task to collect all the plots and summarise as one html page
    yield trs.Task('page', 'page', [('sim', maxIteration, poltEveryNthIteration)])

    # mark this task as completed
    return


# The Function which states how tasks of type 'plot' need to be performed
def rule_plot(TaskKey, TaskData):
    
    # get details on what to plot from task params
    plotDetails = TaskData[0]
    Xs, iteration, maxIteration, poltEveryNthIteration = plotDetails

    # plot the values of x
    h.plot(Xs, iteration, trs.CommonDict['OUTPUT_PATH'])

    # mark this task as completed
    return


# The Function which states how tasks of type 'page' need to be performed
def rule_page(TaskKey, TaskData):

    # get the required details for this task
    _, maxIteration, poltEveryNthIteration = TaskData[-1]

    # collect all the plots and summarise as one html page
    h.collectPlots(maxIteration, poltEveryNthIteration, trs.CommonDict['OUTPUT_PATH'])
    
    # mark this task as completed
    return


# Details about task organisation
trs.NGuests = 4                                 # State that the tasks need to be performed on 4 processes
trs.Rules["init"] = (0, rule_init)              # Declare that there is a task of type 'init' which needs 0 params
trs.Rules["sim"] = (1, rule_sim)                # Declare that there is a task of type 'sim' which needs 1 params
trs.Rules["plot"] = (1, rule_plot)              # Declare that there is a task of type 'plot' which needs 1 param
trs.Rules["page"] = (1, rule_page)              # Declare that there is a task of type 'page' which needs 1 param passed by 'sim' after its complete
trs.InitTask = trs.Task("init", "init", [])     # State that initial task is of type 'init', and does not take any params

# Only the main thread should run this code
if __name__ == '__main__':
    
    # Start execution of the tasks, starting with trs.InitTask
    trs.main()
    
    # Record the number of tasks completed by each process
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

    # Record execution time
    print(f"Completed Execution in: {time.time() - startTimeStamp} secs")
