class deal_queue:
    def __init__(self):
        pass
    def Dispatch_task(self, *info):
        print("info: ", info)
        target = [s for s in info[0] if info[1][0] in s]
        print(target)
        if not target:
            return {"Status": "Busy", "System": info[1], "Message": "Server is Busy, Add Work to Queue"}
        else:
            # take one update status --> Online
            print("Set " + target[0], "Status to busy.")
            delete = target.pop(0)
            # Agent_list delete last take
            print("Delete this: ", delete)
            delete_index = info[0].index(delete)
            del info[0][delete_index]
            # return Agent_list
            return {"Status": "Normal", "data": info[0]}

    def CaseEnd_Update_queue(self, *update):
        # print(update)
        update[0].append(update[1])
        return update[0]

    def Take_Work(self, *Agent_List):
        """""""""
        param: Agent_list, System, System_queue
        1. Check System_queue Is there a job?
            - if System_queue don't have work
                return Work Done
              else:
                Take Work & delete it
                2. Check Is the agent available?
                if not:
                    return "Not idle Agent"
                else:
                    # agent available
                    Take (Job['System'] == Agent System) Work to Do
                    Delete System_queue --> Work
                    Delete Agent_list this Agent
                    Send request tell function do this
        """""""""
        # System_queue don't have your system work
        if len(Agent_List[2]) == 1:
            print(Agent_List[1] in (Agent_List[2][0]))
            if Agent_List[1] in list(Agent_List[2][0].keys()):
                work = Agent_List[2][0][Agent_List[1]]
                print("Work --> ", work)
                Search = [n for n in Agent_List[0] if Agent_List[1] in n]
                if not Search:
                    return "Not idle Agent"
                else:
                    machine = Search.pop(0)
                    print(f"Set machine <{machine}> to Work")
                    Agent_List[0].remove(machine)
                    # print("Check: ", Agent_List[0])
                    del Agent_List[2][0][Agent_List[1]]
                    return work
            else:
                return "Don't have your work"

        elif len(Agent_List[2]) == 0:
            return "No Work"

        else:
            for index, qw in enumerate(Agent_List[2]):
                if Agent_List[1] in list(qw.keys()):
                    work = Agent_List[2][index]
                    break
            Search = [n for n in Agent_List[0] if Agent_List[1] in n]
            if not Search:
                return "Not idle Agent"
            else:
                del Agent_List[2][index]
                work = Agent_List[2][index]
                machine = Search.pop(0)
                Agent_List[0].remove(machine)
                print(f"Set machine {machine} Work")
                return work

