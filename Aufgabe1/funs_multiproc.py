# functions to apply multiprocessing on big datasets
# author: Marvin Luecke
# date: 08.02.22

import os
import math
from multiprocessing import Process, Value, Lock

# def mp_pool(data, mp_function, function):
#     pool = Pool()
#     pool.starmap(mp_function, data)

# main function for the multiprocessing
def mp_settings(data, mp_function, function, defprocs=0):
    procs = []
    score = Value('d', 0.0)
    lck = Lock()
    # set number of processes
    if defprocs == 0:
        processes = int(math.ceil(os.cpu_count() * 0.9))  # default values is 90% of maximum
    else:
        processes = defprocs
    # q = Queue()  # create Queue object to save data
    chunksize = int(math.ceil(len(data) / processes))  # calculate chunksize for each subprocess
    print("Processes used: " + str(processes))
    print("Chunksize: " + str(chunksize))

    for i in range(processes):
        # create subprocesses
        if chunksize * (i + 1) < len(data):
            subdata = data[chunksize * i:chunksize * (i + 1)]
        else:
            subdata = data[chunksize * i:]
        process = Process(target=mp_function, args=(subdata, function, lck, score))
        procs.append(process)
        # start subprocesses
    for proc in procs:
        proc.start()
    # results = {}
    # for i in range(processes):
    #     # write results from the queue to the dictionary results
    #     results.update(q.get())
    for proc in procs:
        # close all the subprocesses (this stops execution of the script, until all processes are finished)
        proc.join()
    # data_new = results[0]
    # for i in range(1, processes):
    #     # combine the results from the queue
    #     data_new = pd.concat([data_new, results[i]], axis=0)
    # return data_new


# adapter functions:
# apply a function on every single row of a dataframe
def mp_apply_adapter(data, function, q, pos):
    print("Process" + str(pos) + " started")
    result = {pos: data.apply(function, axis=1)}
    q.put(result)
    print("Process" + str(pos) + " ended")

# pass the whole dataframe to a function
def mp_whole_adapter(data, function, q, pos):
    print("Process" + str(pos) + " started")
    result = {pos: function(data)}
    q.put(result)
    print("Process" + str(pos) + " ended")
