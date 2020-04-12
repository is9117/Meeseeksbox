# -*- coding: utf-8 -*-

__author__  = "Isaac Park(박이삭)"
__email__ = "is9117@me.com"
__version__ = "0.5"


import sys
import time
import random
import logging
import datetime
import traceback
import threading
import multiprocessing

from threading import Lock
from multiprocessing import Process, Value, Pipe

if sys.version_info[0] < 3:
    from Queue import Empty, Full
else:
    from queue import Empty, Full


__GLOBAL_STOP_FLAG = Value('i', 0, lock=False)

__NAMESPACE_LOCK = Lock()
__NAMESPACE_DATA = {}

__PROCESS_POOL = [] # {"pipe", pipe, "process": process}

__MP_DATA_MANAGER = multiprocessing.Manager()


def new_worker(name, task, init_args=[], input_queue_size=0, output_queue_size=0):

    global __NAMESPACE_DATA, __NAMESPACE_LOCK, __PROCESS_POOL, __MP_DATA_MANAGER
    with __NAMESPACE_LOCK:
        if name in __NAMESPACE_DATA:
            raise Exception("{} namespace already exist".format(name))
    
        # check task compatiblility
        if not hasattr(task, "task"):
            raise Exception("Invalid task input(has no task() function)")

        __NAMESPACE_DATA[name] = {
            "name": name,
            "task": task,
            "args": init_args,
            "input_queue_size": input_queue_size,
            "output_queue_size": output_queue_size,
            "input_queue": __MP_DATA_MANAGER.Queue(input_queue_size),
            "output_queue": __MP_DATA_MANAGER.Queue(output_queue_size)
        }

        __update_process_pool(name)

        return WORKER(name)




def start(worker_num=0):

    global __NAMESPACE_DATA, __NAMESPACE_LOCK, __PROCESS_POOL, __GLOBAL_STOP_FLAG, __MP_DATA_MANAGER
    with __NAMESPACE_LOCK:
        __MP_DATA_MANAGER = multiprocessing.Manager()
        if worker_num == 0:
            worker_num = multiprocessing.cpu_count()
        for _ in range(worker_num):
            parent_conn, child_conn = Pipe()
            internal_worker = __INTERNAL_WORKER_PROCESS(__GLOBAL_STOP_FLAG, child_conn)
            internal_worker.start()
            __PROCESS_POOL.append( {"pipe": parent_conn, "process": internal_worker})
        for name in __NAMESPACE_DATA.keys():
            __update_process_pool(name)

def stop():

    global __NAMESPACE_DATA, __NAMESPACE_LOCK, __PROCESS_POOL, __GLOBAL_STOP_FLAG

    with __NAMESPACE_LOCK:
        __GLOBAL_STOP_FLAG.value = 1
        for worker in __PROCESS_POOL:
            worker["process"].join()
            worker["pipe"].close()
        __PROCESS_POOL.clear()
        __NAMESPACE_DATA.clear()



def put(name, *args):

    global __NAMESPACE_DATA, __NAMESPACE_LOCK, __PROCESS_POOL, __GLOBAL_STOP_FLAG
    with __NAMESPACE_LOCK:
        if name not in __NAMESPACE_DATA:
            raise RuntimeError("namespace {} is invalid(might be removed)".format(name))
        __NAMESPACE_DATA[name]["input_queue"].put(args)


def get(name, count):

    global __NAMESPACE_DATA, __NAMESPACE_LOCK, __PROCESS_POOL, __GLOBAL_STOP_FLAG
    with __NAMESPACE_LOCK:
        if name not in __NAMESPACE_DATA:
            raise RuntimeError("namespace {} is invalid(might be removed)".format(name))
        outputs = []
        for _ in range(count):
            try:
                out = __NAMESPACE_DATA[name]["output_queue"].get_nowait()
                outputs.append(out)
            except Empty:
                break
        return outputs


from .mp_worker import WORKER


# Must call this function 
# inside of 
# __NAMESPACE_LOCK critical section
def __update_process_pool(name):

    global __NAMESPACE_DATA, __PROCESS_POOL

    for p in __PROCESS_POOL:
        p["pipe"].send(__NAMESPACE_DATA[name])



class __INTERNAL_WORKER_PROCESS(Process):
    
    # internal-use members init
    namespace_data = {}
    stop_flag = None
    conn = None

    def __init__( self, stop_flag, conn):
    
        Process.__init__(self)

        self.stop_flag = stop_flag
        self.conn = conn

    def next_namespace(self):

        # add scheduling algorithm here
        # most likely round robin

        names = list(self.namespace_data.keys())
        if names:
            return random.choice(names)
        return None


        
    def run(self):
        
        logging.info("starting worker")

        while True:

            # check break condition
            if self.stop_flag.value is 1:
                # break if all queues are empty
                is_empty_list = [ data["input_queue"].empty() for data in self.namespace_data.values() ]
                if all(is_empty_list):
                    break

            # check data updates
            try:
                while self.conn.poll():
                    data = self.conn.recv()
                    task = data["task"]
                    param = data["args"]
                    instance = task(*param)
                    data["instance"] = instance
                    self.namespace_data[data["name"]] = data
                    logging.info("{} updated".format(data["task"]))
            except EOFError:
                traceback.print_exc()
                pass
        
            try:
                
                namespace = self.next_namespace()
                if not namespace:
                    time.sleep(1)
                    continue
                in_queue = self.namespace_data[namespace]["input_queue"]

                # get job from in queue, if no job found, raises "Empty" exception
                job = in_queue.get_nowait()

                out_queue = self.namespace_data[namespace]["output_queue"]
                worker = self.namespace_data[namespace]["instance"]
                
                # process job with target function
                ret = worker.task(*job)
                
                # returns result to out queue if exists
                if ret is not None:
                    out_queue.put(ret)
                
                # sleep 0 for better multi-processing scheduling optimization
                time.sleep(0)
            
            # if in queue is empty
            except Empty:
                time.sleep(0.1)
            
            # ignore any exceptions other then "Empty"
            except:
                tb = traceback.format_exc()
                logging.error("error occurred at worker main loop : " + tb)


        try:
            self.conn.close()
        except:
            traceback.print_exc()
            pass

        # flush stdout, stdin, stderr
        try:
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdin.flush()
            logging.debug("buffer flushed")
        except:
            tb = traceback.format_exc()
            logging.error("error occurred at flushing buffer : " + tb)
        
        logging.info("ending worker process")
        
        
    




