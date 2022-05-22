import task_ruleset as Lib
import os, sys, time

def rule_init(TaskKey, TaskData):
    return [Lib.Task("get", "get_" + str(i), [i]) for i in range(16)]

def rule_get(TaskKey, TaskData):
    print(TaskKey, TaskData)

Lib.NGuests = 8
Lib.Rules["init"] = (1, rule_init)
Lib.Rules["get"] = (1, rule_get)

Lib.InitTask = Lib.Task("init", "init", ["Hi"])

def main():
    Lib.main()
    print(Lib.TasksAssignedToProcess)

if __name__ == '__main__':
    main()