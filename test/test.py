
import sys
import time
import logging

sys.path.append(".")
import mp


logging.basicConfig(format="%(asctime)s %(levelname)s [%(process)d:%(module)s:%(funcName)s] %(message)s", level=logging.DEBUG)

class Task:

    def task(self, *args):
        logging.info(args)


mp.start()

worker = mp.new_worker("test", Task)

for i in range(100):
    worker.enqueue("test output", str(i))
    time.sleep(0.3)

mp.stop()





