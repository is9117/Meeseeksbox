# -*- coding: utf-8 -*-
import gc
import time
import logging

from mp_manager import MP_MANAGER, WORKER_PROCESS


# top-level function     
def job_function(i):
    time.sleep(0.1)
    print i
    return i, i*2


# class member function
class TEST:

    test_param = "test"
    
    def job_function(self, i):
        time.sleep(0.1)
        print i, self.test_param
        return i, i*3


# PREFORK WORKER_PROCESS test
class TEST_PROCESS(WORKER_PROCESS):

    def __init__(self):
        
        WORKER_PROCESS.__init__(self, enable_log=True, log_level=logging.DEBUG)
        self.test = "abcde"

    def worker_function(self, i):
        time.sleep(0.1)
        print i, self.test
        return i, i*4

        
""" DEFAULT mode test """

# # top-level function
# mp_manager = MP_MANAGER(job_function, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(10):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()
    
# # member function
# test = TEST()
# mp_manager = MP_MANAGER(test.job_function, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(100):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()


""" PREFORK mode test """

# # top-level function
# mp_manager = MP_MANAGER(job_function, mode="PREFORK", enable_log=True, log_level=logging.DEBUG)
# for i in xrange(10):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # member function
# test = TEST()
# mp_manager = MP_MANAGER(test.job_function, mode="PREFORK", enable_log=True, log_level=logging.DEBUG)
# for i in xrange(10):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # instance
# inst = TEST_PROCESS()
# mp_manager = MP_MANAGER(inst, mode="PREFORK", enable_log=True, log_level=logging.DEBUG)
# for i in xrange(10):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()


# # top-level function, reuse mode
# mp_manager = MP_MANAGER(job_function, mode="PREFORK", worker_reuse_num=10, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(100):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # member function, reuse mode
# test = TEST()
# mp_manager = MP_MANAGER(test.job_function, mode="PREFORK", worker_reuse_num=10, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(30):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # instance, reuse mode
# inst = TEST_PROCESS()
# mp_manager = MP_MANAGER(inst, mode="PREFORK", worker_reuse_num=10, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(50):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()



# # top-level function, time-out mode
# mp_manager = MP_MANAGER(job_function, mode="PREFORK", worker_timeout=5, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(300):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # member function, time-out mode
# test = TEST()
# mp_manager = MP_MANAGER(test.job_function, mode="PREFORK", worker_timeout=5, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(300):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # instance, time-out mode
# inst = TEST_PROCESS()
# mp_manager = MP_MANAGER(inst, mode="PREFORK", worker_timeout=5, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(300):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()




# # top-level function, time-out mode and reuse mode
# mp_manager = MP_MANAGER(job_function, mode="PREFORK", worker_reuse_num=100, worker_timeout=50, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(3000):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # member function, time-out mode
# test = TEST()
# mp_manager = MP_MANAGER(test.job_function, mode="PREFORK", worker_reuse_num=100, worker_timeout=5, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(300):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()

# # instance, time-out mode
# inst = TEST_PROCESS()
# mp_manager = MP_MANAGER(inst, mode="PREFORK", worker_reuse_num=100, worker_timeout=5, enable_log=True, log_level=logging.DEBUG)
# for i in xrange(300):
    # mp_manager.put(i)
# mp_manager.stop_all_worker()
# ret = mp_manager.get()
# while ret:
    # print ret
    # ret = mp_manager.get()



""" Termination test """

# __exit__ test
with MP_MANAGER(job_function, enable_log=True, log_level=logging.DEBUG) as mp_manager:
    for i in xrange(10):
        mp_manager.put(i)
    mp_manager.stop_all_worker()


# # __del__ test
# try:
    # mp_manager = MP_MANAGER(job_function, enable_log=True, log_level=logging.DEBUG)
    # for i in xrange(10):
        # mp_manager.put(i)
    # del mp_manager
    # gc.collect()
    # # 잘 안되ㅠㅠ
# except:
    # pass



