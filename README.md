
# MP_MANAGER

version: 0.2.5

date: 2018-02-10


## Summary:
- MP_MANAGER는 python multi-processing worker 관리 라이브러리입니다.
  복수의 worker를 실행, 종료, job분배, worker결과값 추출 등 사용자가 
  손쉽게 worker를 사용, 관리 할 수 있도록 도우는 기능들을 제공하고 있습니다.


## 전체 기능:
- 실행: 
  worker를 최고 입력개수만큼 실행시켜 입력한 job을 multi-processing으로 실행합니다
- 종료: 
  모든 worker가 모든 job을 완료하고 정상 종료될 때 까지 기다려주는 기능을 제공합니다
- job분배: 
  함수 호출하듯 매개변수를 put함수에 입력 시 자동으로 worker들이 job을 받아 실행합니다
- worker결과값 추출: 
  입력한 target(함수/객체, <객체재사용기능> 참고)에서 반환이 있을 경우 get, get_bulk함수로
  결과값을 받을 수 있습니다
- worker재사용 기능: 
  worker프로세스가 job실행 후 종료하지 않고 상시 job을 대기하는 기능을 제공합니다.
  이 기능을 "PREFORK mode"라고 합니다.
  worker프로세스는 매번 fork되거나 객체를 매번 생성해야하는(<객체재사용기능> 참고) overhead를
  줄일 수 있습니다. 특정 객체는 생성 시 비용이 많이 들어 반복 할 만큼 낭비를 할 수 있지만,
  이 기능으로 그런 낭비를 최소화 할 수 있습니다.
- worker reuse limit기능: 
  worker가 일정 개수의 job을 실행 후 재시작 할 수 있는 옵션을 제공합니다.
  이 기능으로 주기적으로 worker를 재시작 할 수 있어 프로세스의 장기간 사용으로 야기되는 행위를 방지할 수 있습니다.
- worker time-out기능: 
  worker가 일정시간이 지난 후 재시작 할 수 있는 옵션을 제공합니다.
  이 기능으로 주기적으로 worker를 재시작 할 수 있어 프로세스의 장기간 사용으로 야기되는 행위를 방지할 수 있습니다.
- 객체재사용기능: 
  mp_manager는 WORKER_PROCESS란 worker클라스를 제공합니다.
  PREFORK mode에서 WORKER_PROCESS를 상속받은 객체를 target으로 넘길 시 객체를 worker life cycle만큼 유지하기 때문에
  불필요한 객채생성 overhead를 줄일 수 있습니다.
  상속받은 클라스는 worker_function 멤버함수를 override하여 필요한 로직을 입력하면 됩니다.
  필요 시 __init__에서나 클라스 멤버로 객체를 생성할 시 재사용이 가능합게 됩니다.
- 로그기능:
  python library인 logging의 logging.handlers와 logging level을 정할 시 mp_manager에서 내부 이벤트를
  로그로 남겨 디버그, 실행시간기록 시 유용합니다.


## 클라스:
<pre><code>class mp_manager.MP_MANAGER(target,
                            worker_num            = 2,
                            input_queue_size      = 4,
                            output_queue_size     = 0,
                            mode                  = "DEFAULT",
                            worker_reuse_num      = 0,
                            worker_timeout        = 0,
                            enable_log            = False,
                            log_handler           = None,
                            log_level             = logging.INFO,
                            log_name              = "mp_manager")</code></pre>
- 설명:
  worker를 관리하는 클라스.
  객체가 생성 시 worker가 같이 생성됩니다(PREFORK mode경우만).
  
- parameters:
  target은 worker가 실행 할 함수나 WORKER_PROCESS상속 객체는 받습니다. "DEFAULT" mode에서는 함수만,
    "PREFORK" mode에서는 함수와 객체를 받을수 있습니다. 
    함수는 어떤 종류가 가능합니다. top-level, class member function 등
  worker_num은 worker의 최고 개수를 정합니다(기본값:2).
  input_queue_size은 입력할 job queue의 크기입니다(기본값:4). 0일 시 무제한이 됩니다. 
    자세한 내용은 링크 참고: [Queue](https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Queue, "multiprocessing.Queue")    
  output_queue_size은 worker가 반환한 결과값을 출력할 queue의 크기입니다(기본값:0). 0일 시 무제한이 됩니다. 
    자세한 내용은 링크 참고: [Queue](https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Queue, "multiprocessing.Queue")
  mode(기본값:"DEFAULT")는 mp_manager의 mode를 결정합니다. PREFORK와 DEFAULT 중 정할 수 있습니다.
  worker_reuse_num는 worker reuse limit를 정합니다(기본값:0). job의 최고 실행 개수를 뜻합니다.
    0 일 시 비활성화 됩니다.
  worker_timeout는 worker의 time-out을 정합니다(기본값:0). job의 실행시간(초단위)을 뜻합니다.
    0 일 시 비활성화 됩니다.
  enable_log(기본값:False)는 로그기능을 활성화 할 지 결정합니다.
  log_handler(기본값:None)는 사용자가 사용할 로그핸들러를 입력할 수 있습니다.
    값이 None일 시 포멧이 "<%(levelname)s::%(name)s> [%(asctime)s] %(message)s"인
    StreamHandler를 사용하게 됩니다.
    자세한 내용은 링크 참고: [handlers](https://docs.python.org/2/library/logging.handlers.html,"logging.handlers")
  log_level(기본값:logging.INFO)는 사용자가 사용할 로그레벨을 입력할 수 있습니다.
    자세한 내용은 링크 참고: [logging](https://docs.python.org/2/library/logging.html,"logging level")
  log_name(기본값:"mp_manager")는 로그 시 사용될 logger객체 이름을 정할 수 있습니다.
    자세한 내용은 링크 참고: [logging](https://docs.python.org/2/library/logging.html)

- 멤버함수
  put_nowait(*args):
    job을 입력합니다. 만약 입력큐가 다 찼을 시 Queue.Full 예외가 발생합니다.
    *args는 target에서 실행하는 함수와 같은 매개변수를 입력하면 됩니다.
    ex) put_nowait('foo', 'bar')
  
  put(*args)
    job을 입력합니다. 만약 입력큐가 다 찼을 시 큐에 공간이 생길 시 까지 hold합니다.
    *args는 target에서 실행하는 함수와 같은 매개변수를 입력하면 됩니다.
    ex) put('foo', 'bar')
  
  get()
    출력큐에서 값을 하나 반환합니다.
    큐가 비었을 경우 None을 반환합니다.
  
  get_bulk(number)
    number개수만큼 출력큐에서 값을 bulk로 반환합니다.
    큐가 비었을 경우 []을 반환합니다.
  
  stop_all_worker()
    모든 worker가 job을 전부 처리하고 종료할 때 까지 기다립니다.
  
  is_inqueue_full()
    입력큐가 찼는지 상태 반환
    
  is_inqueue_empty()
    입력큐가 비었는지 상태 반환
    
  is_outqueue_full()
    출력큐가 찼는지 상태 반환
    
  is_outqueue_empty()
    출력큐가 비었는지 상태 반환


    
<pre><code>class mp_manager.WORKER_PROCESS()</code></pre>

- 설명:
  PREFORK mode에서 객체를 재사용하기 위해서 상속해야 할 클라스.
  worker_function 멤버함수를 override하여 worker로직을 입력하면 됩니다.
  
- 멤버함수:
  worker_function(*args)
    override해야할 함수. 매개변수는 다른 함수에서 쓸 때 와 같이 사용하면 됨
    ex) def worker_function(self, foo, bar):
            # process some job here

            


* * *
## "DEFAULT" mode사용 예제

<pre><code>from mp_manager import MP_MANAGER

def add_func(a, b):
    return a + b

mp = MP_MANAGER(add_func, worker_num=4, input_queue_size=8)

for i in xrange(100):
    mp.put(i, i+1)

ret = mp.get()
while ret:
    print(ret)
    ret = mp.get()
    
mp.stop_all_worker()</code></pre>

* * *
## "PREFORK" mode사용 예제 1

<pre><code>from mp_manager import MP_MANAGER, WORKER_PROCESS

class TEST_WORKER(WORKER_PROCESS):
    foo = FOO() # 재사용할 객체 선언
    
    # override
    def worker_function(self, bar):
        return self.foo.some_function(bar)

test_worker = TEST_WORKER()

# time-out 1h
mp = MP_MANAGER(test_worker, worker_num=4, input_queue_size=8, mode="PREFORK", worker_timeout=60*60)

for i in xrange(100):
    mp.put(i)

ret = mp.get()
while ret:
    print(ret)
    ret = mp.get()

mp.stop_all_worker()</code></pre>

* * *
## "PREFORK" mode사용 예제 2

<pre><code>from mp_manager import MP_MANAGER, WORKER_PROCESS

def print_result(a, b):
    print(a + b)

# worker_reuse_num 5000
mp = MP_MANAGER(print_result, worker_num=4, input_queue_size=8, mode="PREFORK", worker_reuse_num=5000)

for i in xrange(100):
    mp.put(i, i+1)

mp.stop_all_worker()</code></pre>

* * *



