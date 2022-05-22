import Lib
import os, sys, time

def rule_init(TaskKey, TaskData):
    return [Lib.Task("split_a", "split_a", []), Lib.Task("split_b", "split_b", [])]

def rule_split_a(TaskKey, TaskData):
    return [Lib.Task("merge", f"m_{i}", [f"{i}-A;"]) for i in range(8)]
def rule_split_b(TaskKey, TaskData):
    return [Lib.Task("merge", f"m_{i}", [f"{i}-B;"]) for i in range(8)]

def rule_merge(TaskKey, TaskData):
    print(TaskKey, TaskData)

Lib.NGuests = 4
Lib.Rules["init"] = (0, rule_init)
Lib.Rules["split_a"] = (0, rule_split_a)
Lib.Rules["split_b"] = (0, rule_split_b)
Lib.Rules["merge"] = (2, rule_merge)

Lib.InitTask = Lib.Task("init", "init", [])

def main():
    Lib.main()
    print(Lib.TasksAssignedToProcess)

if __name__ == '__main__':
    main()