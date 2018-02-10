
import time
import logging
import traceback
import threading

from copy import copy
from Queue import Empty
from multiprocessing import Process, Queue, Value


class TEST:

    b = "bcde"

    def test(self, a):
        print a, self.b

        
def func(target, a):

    print callable(target)

    # target(a)
    
if __name__ == "__main__":

    # t = TEST()
    
    # func(t.test, 'ajklkj')
    # func(t, 'ajklkj')
    
    # print "{}".format(t.test)

    in_q_dict = {}
    for i in xrange(10):
        in_q_dict[i] = {'cnt':i, 'queue':None}
        
    print in_q_dict
    
    print in_q_dict.values()
    
    new_list = sorted(in_q_dict.values(), key=lambda x: x['cnt'], reverse=True)
    # new_list = sorted(in_q_dict.values(), key=attrgetter('cnt'), reverse=True)
    print new_list
    
    new_list[0]['cnt'] += 1
    in_q_dict[0]['cnt'] += 1
    
    print new_list
    print in_q_dict
    
    
    