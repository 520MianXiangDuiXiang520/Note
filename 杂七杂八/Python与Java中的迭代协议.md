# 迭代协议

迭代协议（Iteration protocol）包含两部分内容：

1. 可迭代对象协议（Iterable protocol）：实现了该协议的对象叫做可迭代对象（Iterable ）
2. 迭代器协议（Iterator protocol）：实现了该协议的对象叫做迭代器（Iterator ）

## 迭代器协议（Iterator protocol）

迭代器协议允许我们使用`next()`方法逐个访问集合中的每个元素，直到到达了集合末尾，`next()`方法将会抛出一个异常。

在Java中，通过实现`Iterator`接口实现迭代器协议

```java
package Note.cistern;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class MyIterator implements Iterator {
    int start, end, step;

    public MyIterator(int start, int end, int step) {
        this.start = start;
        this.end = end;
        this.step = step;
    }

    public MyIterator(int start, int end) {
        this(start, end, 1);
    }
    public MyIterator(int end) {
        this(0, end, 1);
    }

    @Override
    public boolean hasNext() {
        return this.start < this.end;
    }

    @Override
    public Object next() {
        int now;
        if (this.start < this.end){
            now = this.start;
            this.start ++;
            return now;
        } else {
            throw new NoSuchElementException();
        }
    }

    public static void main(String[] args) {
        MyIterator myIterator = new MyIterator(10);
        while(myIterator.hasNext()) {
            System.out.println(myIterator.next());
        }
    }
}

```



## 可迭代对象协议（Iterable protocol)

如果一个对象是可迭代对象，在Java中他就表现为能使用`for each`语法进行迭代，而在python中，`in`关键字后面跟的对象就必须是可迭代对象。

### Java中实现Iterable protocol

Java中凡是实现了`Interable`接口的类都是可迭代对象