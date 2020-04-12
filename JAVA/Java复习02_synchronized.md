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

## 陆. Synchronized和ReentrantLock的区别

## 柒. Java 6 对Synchronized的优化

### 1. 偏向锁

### 2. 轻量级锁

### 3. 自旋锁

### 4. 重量级锁

### 5. 锁粗化

## 捌. 使用Synchronized时的优化







