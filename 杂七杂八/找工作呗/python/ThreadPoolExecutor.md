```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep


def get_html(name):
    sleep(2)
    print(f"{name} get ok")


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(get_html, ("first", ))
    task2 = executor.submit(get_html, ("second",))

```

## `__init__`方法

```python
    def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):
        if max_workers is None:
            # 不指定最大线程数，默认使用CPU核心数*5
            max_workers = (os.cpu_count() or 1) * 5
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        if initializer is not None and not callable(initializer):
            raise TypeError("initializer must be a callable")

        self._max_workers = max_workers
        self._work_queue = queue.SimpleQueue()
        self._threads = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))
        self._initializer = initializer
        self._initargs = initargs
```

初始化ThreadPoolExecutor对象时，可以传递max_workers，用来表示线程池中最多允许的线程数，如果不指定，默认使用CPU核心数*5

## submit 源码解析

submit的作用是往线程池中添加一个线程并执行，如果线程池已满就阻塞。执行后立刻返回一个Future对象，该对象中包含线程执行后的所有信息。



```python
    def submit(self, fn, *args, **kwargs):
        # 调用submit时，需要获得一个不可重入锁
        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _shutdown:
                raise RuntimeError('cannot schedule new futures after'
                                   'interpreter shutdown')

            # 实例化一个Future对象
            f = _base.Future()
            # 实例化一个_WorkItem对象，传递上面的Future对象和线程执行的函数fn
            w = _WorkItem(f, fn, args, kwargs)
			# 将_WorkItem对象加入到工作线程的队列中
            self._work_queue.put(w)
            self._adjust_thread_count()
            # 返回Future对象
            return f
```

```python
    def _adjust_thread_count(self):
        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)
        
        num_threads = len(self._threads)
        # 如果线程池中的线程数小于最大线程数，就创建一个新线程并执行
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
            # 创建的这个线程执行的方法是_worker()
            t = threading.Thread(name=thread_name, target=_worker,
                                 args=(weakref.ref(self, weakref_cb), # 将一个self的弱引用对象传递给_worker()
                                       self._work_queue,
                                       self._initializer,
                                       self._initargs))
            # 以守护线程方式执行
            t.daemon = True
            t.start()
            # 将这个线程加入到_threads集合
            self._threads.add(t)
            _threads_queues[t] = self._work_queue
```

```python
def _worker(executor_reference, work_queue, initializer, initargs):
    if initializer is not None:
        try:
            initializer(*initargs)
        except BaseException:
            _base.LOGGER.critical('Exception in initializer:', exc_info=True)
            executor = executor_reference()
            if executor is not None:
                executor._initializer_failed()
            return
    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run()
                # Delete references to object. See issue16284
                del work_item
                continue
            executor = executor_reference()
            # Exit if:
            #   - The interpreter is shutting down OR
            #   - The executor that owns the worker has been collected OR
            #   - The executor that owns the worker has been shutdown.
            if _shutdown or executor is None or executor._shutdown:
                # Flag the executor as shutting down as early as possible if it
                # is not gc-ed yet.
                if executor is not None:
                    executor._shutdown = True
                # Notice other workers
                work_queue.put(None)
                return
            del executor
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)
```

