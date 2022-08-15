import task_ruleset as trs
import os, sys, time
import pathlib
from matplotlib import pyplot

nameOfThisFile = "001_SimpleSplit.py"

def rule_init(TaskKey, TaskData):
    
    root = pathlib.Path.cwd()
    print(f"{TaskKey} - Listing files in {pathlib.Path.cwd()}")

    foundThisFile = False
    listTextFiles = []

    for item in os.listdir(root):
        if os.path.isfile(itemPath := os.path.join(root, item)):
            if item == nameOfThisFile:
                foundThisFile = True
            elif item.endswith(".txt"):
                listTextFiles.append((item, itemPath))
    
    if not foundThisFile:
        print(f"{TaskKey} - ERROR : Current directory does not contain file {nameOfThisFile}! Exiting.")
        return
    
    print(f"{TaskKey} - Following files will be processed:")
    for textFile in listTextFiles:
        print(f"{TaskKey} -     {textFile[1]}")
    
    NewTasks = []
    for i, textFile in enumerate(listTextFiles):
        NewTasks.append(
            trs.Task(
                "proc",
                f"proc_{i}",
                [textFile]
            )
        )
    return NewTasks


def rule_proc(TaskKey, TaskData):

    fileName, filePath = TaskData[0]
    print(f"{TaskKey} - Processing file : {fileName}")
    
    plotFileName = fileName.split('.')[0] + "_plot.png"

    X = []; Y = []
    Xl = 'X  ->'; Yl = 'Y  ->'
    with open(filePath) as data:
        dataLines = data.readlines()

        header, *otherLines = dataLines
        Xl, Yl = header.split()

        for o in otherLines:
            x, y = map(float, o.split())
            X.append(x); Y.append(y)

    pyplot.figure(1, (6, 6))
    pyplot.scatter(X, Y)
    pyplot.xlabel(Xl); pyplot.ylabel(Yl)
    pyplot.savefig(plotFileName)
    print(f"{TaskKey} - Saved file as : {plotFileName}")

    return


trs.NGuests = 8
trs.Rules["init"] = (0, rule_init)
trs.Rules["proc"] = (1, rule_proc)
trs.InitTask = trs.Task("init", "init", [])

def main():
    print("main - Starting Execution")
    trs.main()
    print("main - Tasks completed by each process :", trs.TasksAssignedToProcess)

if __name__ == '__main__':
    main()
