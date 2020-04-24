His flower had told him that she was only one of her kind in all universe. And here were five thousand of them, all alike, in one single garden!

<!-- more -->

# Java Synchronized 关键字

## 壹. Java并发编程存在的问题

### 1. 可见性问题

可见性问题是指一个线程不能立刻拿到另外一个线程对共享变量的修改的结果。

如：

```java
package Note.concurrency;

public class Demo07 {
    private static boolean s = true;
    public static void main(String[] args) {

        new Thread(() -> {
            while(s) {

            }

        }).start();

        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        new Thread(() -> {
            s = false;

        }).start();
        System.out.println(s);
    }
}

```

运行之后，第一个线程一直没有停止，说明第二个线程对s的修改没有立刻被线程1拿到

### 2. 原子性问题

原子性问题是指一条Java语句有可能会被编译成多条语句执行，多线程环境下修改同一个变量就会导致结果错误，如：

```java
package Note.concurrency;

import java.util.ArrayList;
import java.util.List;

public class Demo08 {
    private static int num = 0;
    public static void main(String[] args) {
        Runnable runnable = () -> {
            num ++;
        };

        List<Thread> list = new ArrayList<Thread>();
        for (int i = 0; i < 5; i++) {
            Thread thread = new Thread(runnable);
            thread.start();
            list.add(thread);
        }

        for (Thread t :list) {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println(num);
    }
}//~ 4

```

由于`++`不是原子性操作，通过反编译，一个自增语句会被翻译成四条语句执行：

```java
private static void lambda$main$0();
    descriptor: ()V
    flags: ACC_PRIVATE, ACC_STATIC, ACC_SYNTHETIC
    Code:
      stack=2, locals=0, args_size=0
         0: getstatic     #16                 // Field num:I
         3: iconst_1
         4: iadd
         5: putstatic     #16                 // Field num:I
         8: return
      LineNumberTable:
        line 10: 0
        line 11: 8

```



### 3. 有序性问题

Java编译时会优化代码，这时如果两个无关联的语句Java可能会调整他的顺序，导致有序性问题。

## 贰. 线程状态

![UTOOLS1586703796900.png](http://yanxuan.nosdn.127.net/077726a85c16ebe019b1ec073db4f911.png)

![UTOOLS1586591638004.png](http://yanxuan.nosdn.127.net/1227d8066958a7b98b619f919e54195a.png)

## 叁. Synchronized的用法

### 1. 修饰成员方法

在定义成员方法时添加关键字`Synchronized`可以保证同时只有一个线程执行此成员方法，线程进入成员方法时，需要先获取锁，方法执行完毕后，会自动释放锁，Synchronized修饰成员方法时，使用的锁对象是`this`

### 2. 修饰静态方法

因为静态方法所有实例共享一份，所以相当于给类加锁，锁对象默认是当前类的字节码文件，所以用`Synchronized`修饰的成员方法和静态方法是可以并发运行的。

例：双重检验锁实现线程安全的单例模式：

```java
package Note.concurrency;

public class Singleton {
    private volatile static Singleton singleton;

    private Singleton(){}

    public static Singleton getSingleton() {
        if (singleton == null) {
            synchronized (Singleton.class) {
                if(singleton == null)
                    singleton = new Singleton();
            }
        }
        return singleton;
    }
}

```

* `singleton = new Singleton();`不是原子操作，会被翻译成下面四句之类，为保证线程安全，需要放在synchronized代码块中。

```java
17: new           #3                  // class Note/concurrency/Singleton
20: dup
21: invokespecial #4                  // Method "<init>":()V
24: putstatic     #2                  // Field 
```

* 为了避免不可见性问题，共享变量使用Volatile关键字修饰


### 3. 修饰代码块

修饰代码块时，要指定锁对象，可以是任意的Object对象（尽量不要是String xxx , 因为String池有缓存），每个线程需要执行`Synchronized`代码块中的代码时，要先获取锁对象，否则就会被阻塞， 代码块结束，锁对象自动释放。

## 肆. Synchronized的特性

### 1. 可重入

`Synchronized`是一个可重入锁，意思是在获得锁后可以再次获得该锁而不会陷入死锁

```java
package Note.concurrency;

public class ReentrantLockDemo {
    private int num = 0;
    final Object object = new Object();

    private void method1() {
        synchronized (object) {
            num ++;
        }
    }

    private void method2() {
        synchronized (object) {
            method1();
        }
    }

    public static void main(String[] args) {
        ReentrantLockDemo reentrantLockDemo = new ReentrantLockDemo();
        new Thread(reentrantLockDemo::method2).start();
        new Thread(reentrantLockDemo::method2).start();
    }
}
```



### 2. 不可中断

如果有A，B两个线程竞争锁，如果使用Synchronized，A获得锁后，如果不释放，B将一直等下去，不能中断。

```java
package Note.concurrency;

public class UninterruptibleDemo {
    private static final Object o = new Object();

    public static void main(String[] args) throws InterruptedException {
        // 线程1 拿到锁后阻塞3s
        new Thread(() -> {
            synchronized (o) {
                System.out.println("线程1的同步代码块开始执行");
                try {
                    Thread.sleep(6000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(" 线程1的同步代码块执行结束");
            }
        }).start();

        // 让线程1先执行
        Thread.sleep(100);

        Thread t2 = new Thread(() -> {
            synchronized (o) {
                System.out.println("线程2的同步代码块开始执行");
            }

        });
        t2.start();

        // 主线程休眠3s后，锁o 依然被线程1拿着，线程2处于BLOCKED状态
        Thread.sleep(3000);
        System.out.println("线程2的状态：" + t2.getState());

        // 尝试中断线程2，如果synchronized允许被中断，那线程2此时的状态应该会变为Terminated（死亡）状态
        // 反之synchronized如果不可中断，线程2的状态会保持BLOCKED（阻塞）状态
        t2.interrupt();

        System.out.println("线程2的状态：" + t2.getState());

    }
}

//线程1的同步代码块开始执行
//线程2的状态：BLOCKED
//线程2的状态：BLOCKED
//线程1的同步代码块执行结束
//线程2的同步代码块开始执行

```



## 伍. Synchronized的原理

通过javap反汇编一下代码

```java
package Note.concurrency;

public class Demo10 {
    public static synchronized void testMethod() {
    }
    public static void main(String[] args) {
        testMethod();
        synchronized(Demo10.class) {
            System.out.println("");
        }
    }
}

```

可以看到，通过Synchronized修饰的代码块：

```java
 public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=3, args_size=1
         0: ldc           #2                  // class Note/concurrency/Demo10
         2: dup
         3: astore_1
         4: monitorenter
         5: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
         8: ldc           #4                  // String
        10: invokevirtual #5                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        13: aload_1
        14: monitorexit
        15: goto          23
        18: astore_2
        19: aload_1
        20: monitorexit
        21: aload_2
        22: athrow
        23: return
Exception table:
    from    to  target type
       5    15    18   any
      18    21    18   any


```

对比普通语句，多了`monitorenter`和`monitorexit`,`monitorenter`是同步代码块开始的地方，`monitorexit`是同步代码块结束的地方，当线程运行到`monitorenter`后，会试图获取`monitor`对象，这个对象定义在JVM层（是一个C++的对象），每个Java对象都可以和一个monitor关联，这个monitor对象保存在Java对象的对象头中（这也是为什么任意的object对象都可以作为锁的原因），这个monitor对象中有一个`recursions`属性，用来保存被锁的次数，第一次运行到`monitorenter`时，检查要获取的锁关联的monitor对象的`recursions`是不是0，如果是0，说明该锁没有被任何人获取，就可以获取锁，把锁的`recursions`加一，并将monitor对象的`owner`属性设置为当前的Java对象。当执行`monitorexit`时， 会将`recursions`减一，当`recursions`减为0时，标志着当前占有锁的线程释放锁。

> 第20行还有一个`monitorexit`，最下面的异常表显示，如果5到15行发生异常，从18行开始执行，说明如果同步代码块中发生异常， 锁会被自动释放。

### synchronized修饰方法的情况

```java
  public static synchronized void testMethod();
    descriptor: ()V
    flags: ACC_PUBLIC, ACC_STATIC, ACC_SYNCHRONIZED
    Code:
      stack=0, locals=0, args_size=0
         0: return
      LineNumberTable:
        line 5: 0

```

如果使用synchronized修饰方法，该方法会被添加上`ACC_SYNCHRONIZED`标记，添加了该标记的方法在执行时会隐式的调用`monitorenter`和`monitorexit`

## 陆. Synchronized和ReentrantLock的区别

1. Synchronized是一个关键字，依赖于JVM，而ReentrantLock是一个类，依赖于API；
2. Synchronized可以修饰方法，ReentrantLock只能修饰代码块；
3. synchronized可以自动释放锁，哪怕被它修饰的方法或代码块发生异常，它也可以把锁释放了，但ReentrantLock需要手动调用`unlock()`释放锁，与`try...finally`配合使用，避免死锁；
4. ReentrantLock有比Synchronized更丰富的功能，如：
   * ReentrantLock可以做公平锁，也可以做非公平锁，但Synchronized就是非公平锁。
   * ReentrantLock可以判断对象有没有拿到锁。
   * ReentrantLock提供了一种能够中断等待锁的线程的机制，通过`lock.lockInterruptibly()`等待锁的线程可以放弃等待锁去干别的事情。
   * Lock可以通过使用读锁提高性能。

## 柒. Java 6 对Synchronized的优化

### 1. 偏向锁

大多数情况下，锁总是右同一线程多次获得，不存在线程竞争，所以偏向锁就是适用于这种情况，当有线程第一次获取锁时，JVM会把对象头中的标志位设置为01，即偏向模式，并且将线程ID记录下来，以后线程每次访问同步代码块只需要判断线程ID是不是记录的偏向线程的ID，如果是就直接不进行同步了。但如果一旦发生线程竞争，偏向锁就会升级为轻量级锁。由于偏向锁只能在全局安全点（所有线程全部停止）撤销，所以在存在线程竞争的环境下使用偏向锁会得不偿失。

> 在JDK5中偏向锁默认是关闭的，而到了JDK6中偏向锁已经默认开启。但在应用程序启动几秒钟之后才 激活，可以使用 -XX:BiasedLockingStartupDelay=0 参数关闭延迟，如果确定应用程序中所有锁通常 情况下处于竞争状态，可以通过 XX:-UseBiasedLocking=false 参数关闭偏向锁。

### 2. 轻量级锁

偏向锁失效后会升级为轻量级锁，轻量级锁适用于线程交替执行同步代码块的情况下，它使用CAS操作代替重量级锁使用操作系统互斥变量的操作，因此避免了程序频繁在系统态和用户态之间切换的开销，但之所以使用轻量级锁，是基于“**对于绝大部分锁，在整个同步周期内都是不存在竞争的**”的经验数据，如果有多个线程同时进入临界区，那CAS操作的效率可能反而不如重量级锁，如果存在线程竞争，轻量级锁就会膨胀为重量级锁。

### 3. 自旋锁

一般情况下，同步代码块中的代码执行时间都比较短，所以一时间获取不到锁，可能再重试一次就可以了，而不用升级为重量级锁，自旋锁就是基于这个原理，它允许获取不到锁的线程重复几次尝试获取锁，默认是10次，JDK 1.6 开始加入自适应自旋锁，会根据之前自旋的情况动态确定自旋的次数。

### 4. 重量级锁

经过自旋后还是获取不到锁，那就会升级为重量级锁，也就是`monitor`

### 5. 锁消除

> 锁消除理解起来很简单，它指的就是虚拟机即使编译器在运行时，如果检测到那些共享数据不可能存在竞争，那么就执行锁消除。锁消除可以节省毫无意义的请求锁的时间。

### 5. 锁粗化

> JVM会探测到一连串细小的操作都使用同一个对象加锁，将同步代码块的范围放大，放 到这串操作的外面，这样只需要加一次锁即可。

## 捌. 使用Synchronized时的优化

1. 减少Synchronized的范围，让同步代码块中的代码执行时间尽可能短
2. 降低锁粒度，将一个大锁改为多个不同锁对象的小锁，如HashTable和ConcurrentHashMap
3. 读写分离，读不加锁，写加锁。

## 拾. 参考

[https://gitee.com/SnailClimb/JavaGuide/blob/master/docs/java/Multithread/synchronized.md](https://gitee.com/SnailClimb/JavaGuide/blob/master/docs/java/Multithread/synchronized.md)

[https://www.bilibili.com/video/BV1aJ411V763](https://www.bilibili.com/video/BV1aJ411V763)





