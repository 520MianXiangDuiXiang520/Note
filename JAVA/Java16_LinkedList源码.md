# LinkedList源码

LinkedList内部实现是链表，相比ArrayList增删更快，但查找较慢

node节点源码

```java
private static class Node<E> {
    // 数据
    E item;
    // 前驱节点
    Node<E> next;
    // 后继节点
    Node<E> prev;

    Node(Node<E> prev, E element, Node<E> next) {
        this.item = element;
        this.next = next;
        this.prev = prev;
    }
}
```

属性

```java
// list中实际的元素个数
transient int size = 0;
// 头节点
transient Node<E> first;
// 尾节点
transient Node<E> last;
```

add(E e)方法

```java
public boolean add(E e) {
    // 将元素作为最后一个节点加入链表
    linkLast(e);
    return true;
}
```

```java
void linkLast(E e) {
    final Node<E> l = last;
    // 新建一个节点
    final Node<E> newNode = new Node<>(l, e, null);
    last = newNode;
    if (l == null)
        // 针对创建第一个节点的情况
        first = newNode;
    else
        l.next = newNode;
    size++;
    modCount++;
}
```

remove(Object o)方法

```java
public boolean remove(Object o) {
    // 防止NPL
    if (o == null) {
        for (Node<E> x = first; x != null; x = x.next) {
            if (x.item == null) {
                unlink(x);
                return true;
            }
        }
    } else {
        for (Node<E> x = first; x != null; x = x.next) {
            if (o.equals(x.item)) {
                unlink(x);
                return true;
            }
        }
    }
    return false;
}
```

```java
E unlink(Node<E> x) {
    // assert x != null;
    final E element = x.item;
    final Node<E> next = x.next;
    final Node<E> prev = x.prev;
    // 如果前驱节点为空，说明是第一个，就把下一个节点作为首节点
    if (prev == null) {
        first = next;
    } else {
        // 如果是中间节点，就把它前驱节点的next指向后继节点，将自己的prev指针指向null
        prev.next = next;
        x.prev = null;
    }

    // 要删除最后一个节点的情况
    if (next == null) {
        last = prev;
    } else {
        next.prev = prev;
        x.next = null;
    }

    // 引用指向null， 让改节点被回收
    x.item = null;
    size--;
    modCount++;
    // 返回删除掉的节点的值
    return element;
}
```

通过下标删除

```java
public E remove(int index) {
    // 检查index是否合法
    checkElementIndex(index);
    return unlink(node(index));
}
```

```java
Node<E> node(int index) {
    // assert isElementIndex(index);

    // 如果index在前半部分，就从前往后找，否则就从后往前找
    if (index < (size >> 1)) {
        Node<E> x = first;
        for (int i = 0; i < index; i++)
            x = x.next;
        return x;
    } else {
        Node<E> x = last;
        for (int i = size - 1; i > index; i--)
            x = x.prev;
        return x;
    }
}
```

addAll()方法

```java
public boolean addAll(int index, Collection<? extends E> c) {
    // index传进来的是size, 也就是新添加的元素都在末尾
    checkPositionIndex(index);

    Object[] a = c.toArray();
    int numNew = a.length;
    if (numNew == 0)
        return false;

    Node<E> pred, succ;
    if (index == size) {
        succ = null;
        pred = last;
    } else {
        succ = node(index);
        pred = succ.prev;
    }

    for (Object o : a) {
        @SuppressWarnings("unchecked") E e = (E) o;
        Node<E> newNode = new Node<>(pred, e, null);
        if (pred == null)
            first = newNode;
        else
            pred.next = newNode;
        pred = newNode;
    }

    if (succ == null) {
        last = pred;
    } else {
        pred.next = succ;
        succ.prev = pred;
    }

    size += numNew;
    modCount++;
    return true;
}
```



