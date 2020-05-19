# python协程和异步IO

## 协程

协程也叫微线程，是一种在用户态内的上下文切换技术，也就是在一个线程内实现代码块的相互切换执行

python实现协程的办法：

* yield
* greenlet或gevent
* asyncio python3.4加入
* async 和 await 关键字， python3.5加入

### greenlet

```python
from greenlet import greenlet


def func1():
    print("1")
    gl2.switch()  # 切换到func2
    print("11")
    gl2.switch()


def func2():
    print("2")
    gl1.switch()  # 切换到func1
    print("22")
    gl1.switch()


if __name__ == '__main__':
    gl1 = greenlet(func1)
    gl2 = greenlet(func2)
    gl1.switch()
    
    # 1 2 11 22

```

## async 和 await

