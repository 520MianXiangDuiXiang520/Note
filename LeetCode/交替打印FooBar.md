# 交替打印FooBar

```py
from threading import Condition
class FooBar:
    def __init__(self, n):
        self.n = n
        self._lock = Condition()
    def foo(self, printFoo) -> None:
        with self._lock:
            for i in range(self.n):
                printFoo()
                self._lock.wait()
                self._lock.notify()
    def bar(self, printBar) -> None:
        with self._lock:
            for i in range(self.n):
                printBar()
                self._lock.notify()
                self._lock.wait()
```
