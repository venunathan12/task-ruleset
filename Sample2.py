import Lib
import os, sys, time

def rule_init(TaskKey, TaskData):
    return [Lib.Task("get", "get_" + str(i), [i]) for i in range(16)]

def rule_get(TaskKey, TaskData):
    time.sleep(1)
    print(TaskKey, TaskData, Lib.ProcessDict)

Lib.NGuests = 8
Lib.Rules["init"] = (0, rule_init)
Lib.Rules["get"] = (1, rule_get)

Lib.InitTask = Lib.Task("init", "init", [])

def ProcessInit(id):
    Lib.ProcessDict["ID"] = id
Lib.ProcessInit = ProcessInit

def main():
    print("Starting Execution")
    Lib.main()
    print(Lib.TasksAssignedToProcess)

if __name__ == '__main__':
    main()