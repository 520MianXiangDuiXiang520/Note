# Dog planing Notes

![to love to attempt](/image/attempt.png)

---

## python

1. 数据类型：

  * 可变类型：list, dict, set
  * 不可变类型：int, float, string, tuple

  * dict的实现：Hash Table,开放地址法解决冲突
  * 鸭子类型：只关心对象行为，而不关心对象类型
  * 反射，自省：
    * 反射：操纵对象的能力，`setattr()`
    * 自省：获取对象的能力, `getattr()`, `isinstance()`, `type()`, `callable()`...
  * 序列解包
  ```py
  s = "abcde"
  a, b, c, d, e = s
  print(a, c)  # (a, c)
  ```
  * 格式化字符串（%，format, f-string）

2. 循环结构
  
  * while循环
  * 迭代器，可迭代对象，生成器
    * 可迭代对象：可以直接作用于for循环的对象，内部实现了`__iter__()`方法。该方法返回一个迭代器。
    * 迭代器：实现了`__next__()`方法的对象，该方法返回迭代的下一个元素，没元素时抛出`StopIteration`异常，外部调用`next()`方法获取下一个元素，for循环也是捕获到这个异常就停止向下遍历。
    * 生成器：可以使用`(i for i in range(10))`这样创建，同时函数中出现`yield`时，这个函数就成了生成器，生成器是可迭代对象

    ```py
    class MyRange:
      def __init__ (self, end:int, start: int=None, step:int=None):
          if start:
              self.start = end
              self.end = start
              self.step = 1 if not step else step
          else:
              self.start = 0
              self.end = end
              self.step = 1
          
      def __iter__(self):
          return self

      def __next__(self):
          if self.start >= self.end:
              raise StopIteration
          next_int = self.start
          self.start += self.step
          return next_int


      if __name__ == '__main__':
          for i in MyRange(20):
              print(i)
    ```

3. 分支结构

  * 布尔表达式

  ```py
   return 1 if a is True else 2
  ```

4. 函数

  * 参数传递: 传对象的引用
  * python重载的实现：单分派泛型函数 `from functools import singledispatch`
  * lambda 表达式 `var = lambda x, y:x + y`
  * 函数式编程
  * 类型注释

5. 面向对象

  * 静态方法，类方法，属性方法，实例方法
  * 魔术方法
  * type和Metaclass

6. 多任务

  * 多线程：
    * GIL全局解释器锁
    * 生产者消费者模型
    * 多线程UDP通信
  * 多进程
    * 僵尸进程（父进程未死但不处理子进程）和孤儿进程（父进程已死）
    * 进程间通信：管道，共享内存，队列
  * 协程
    * yield实现协程
    * greenlet 实现协程
    * gevent实现协程

7. 闭包和装饰器
  
  * 闭包？内部函数调用了外部函数作用域内的变量
  * 三种类型的装饰器
  * AOP：面向切面编程，横向拓展

8. GC机制

  * 引用计数
  * 标记清除：解决引用计数无法回收循环引用对象的问题
  * 分代回收：弱代假说

9. 异常机制

  * 异常继承体系
  * try,except,else,finally
  * 断言access

10. 常用模块

  * os与sys：os操作系统相关。sys编译器相关
  * requests

10. 其他

  * 设计模式
  * PEP8
  * 上下文管理器
  * python2与python3？

## Nginx

1. 配置文件
2. 反向代理
3. 负载均衡
4. 动静分离
5. 高可用集群

## Docker

1. 三要素：仓库，镜像，容器
2. 常用命令
3. DockerFile

## Django

1. CBV FBV
2. Model, ORM
3. URL调度
4. MVC MVVM

## Rest

1. Restful规范
2. 为什么前后端分离
3. django-Rest-Fearmwork源码
  * 入口: dispatch
  * 模块：认证，授权，节流，分页，序列化，版本
4. 跨域的解决办法：前端代理，CORS认证

## Linux

1. 常用命令
2. 用户和组管理
3. 进程管理
4. vi和vim

## 计算机网络

1. TCP/IP 分层模型
2. HTTP和HTTPS
3. HTTP状态码
4. 三次握手，四次挥手

## 数据库

1. 事务？四大特性？
2. 隔离级别：脏读，不可重复读，幻读
3. 索引？
  
  * 聚簇索引
  * 非聚簇索引

4. 锁：乐观锁，悲观锁，排它锁
5. 存储过程，触发器

## 网络安全

1. 常见攻击

  * SQL注入
  * XSS
  * CSRF

2. 密码学

## Java

1. 数据类型

  * 拆装箱

2. 字符串与正则
3. 访问权限控制
4. 抽象类，接口，内部类，匿名内部类，继承，实现
5. 容器
6. 反射
7. IO
8. 多线程
9. GC
10. JVM

## JavaScript

1. DOM和BOM
2. 原型和原型链
3. 执行上下文和执行上下文栈
4. 闭包
5. 匿名函数
6. ES6



