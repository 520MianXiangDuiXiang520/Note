# ArrayList 源码分析

```java
package Note.cistern;

import java.util.ArrayList;

public class ArrayListDemo {
    public static void main(String[] args) {
        ArrayList<Object> arrayList = new ArrayList<>();
        arrayList.add("e");
    }
}
```

属性和构造方法：

```java
 private static final long serialVersionUID = 8683452581122892189L;

    /**
     * 默认的初始容量
     */
    private static final int DEFAULT_CAPACITY = 10;

    /**
     * 初始化一个空实例时的数组
     */
    private static final Object[] EMPTY_ELEMENTDATA = {};

    /**
     *缺省空对象数组
     */
    private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};

    /**
     * 保存数据的数组变量
     */
    transient Object[] elementData;

    /**
     * arrayList中实际的元素个数
     */
    private int size;
```



```java
public ArrayList() {
    // 使用默认构造函数实例化ArrayList时，先初始化一个空数组
    // 相当于 this.elementData = 
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}
```

add(E e)方法

```java
public boolean add(E e) {
    // 该方法用来确保数组够用
    // 因为要保证剩余空间够放下一个新元素，所以要对size + 1判断
    ensureCapacityInternal(size + 1);
    // 把新元素放入数组，实际大小加一
    elementData[size++] = e;
    return true;
}
```

```java
private void ensureCapacityInternal(int minCapacity) {
    ensureExplicitCapacity(calculateCapacity(elementData, minCapacity));
}
```
```java
private static int calculateCapacity(Object[] elementData, int minCapacity) {
    // 如果数组elementData是空的（第一次添加数据）时
    if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        // 返回DEFAULT_CAPACITY（默认10）和minCapacity（调用）的最大值
        return Math.max(DEFAULT_CAPACITY, minCapacity);
    }
    // 否则直接返回minCapacity
    return minCapacity;
}
```

```java
private void ensureExplicitCapacity(int minCapacity) {
    modCount++;

    // 对于第一次来说，minCapacity=10， elementData.length = 0
    // 这时elementData还是一个空数组，需要扩容才能放下新数据
    if (minCapacity - elementData.length > 0)
        // 扩容
        grow(minCapacity);
}
```

```java
private void grow(int minCapacity) {
    // 旧的容量
    int oldCapacity = elementData.length;
    // 新容量是旧的的基础上扩容50%
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    // 针对第一次扩容的情况，这时oldCapacity=0， newCapacity=0
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    // 如果扩容后超过了最大容量限制
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        // 分配最大容量
        newCapacity = hugeCapacity(minCapacity);
    // 新容量确定，copy一个新容量的数组给ArrayList
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

```java
private static int hugeCapacity(int minCapacity) {
    if (minCapacity < 0) // overflow
        throw new OutOfMemoryError();
    // 把能分配的最大容量分配给容器
    return (minCapacity > MAX_ARRAY_SIZE) ?
        Integer.MAX_VALUE :
    MAX_ARRAY_SIZE;
}
```

其他add方法实现也大同小异，

```java
public void add(int index, E element) {
    // 检查index是不是在规定范围内
    rangeCheckForAdd(index);
    // 确保容量够用
    ensureCapacityInternal(size + 1); 
    // 插入新元素
    System.arraycopy(elementData, index, elementData, index + 1,
                     size - index);
    elementData[index] = element;
    size++;
}
```

```java
public boolean addAll(Collection<? extends E> c) {
    // Collection对象转换为数组
    Object[] a = c.toArray();
    int numNew = a.length;
    ensureCapacityInternal(size + numNew);  // Increments modCount
    // 合并两个数组
    System.arraycopy(a, 0, elementData, size, numNew);
    size += numNew;
    return numNew != 0;
}
```

```java
public boolean addAll(int index, Collection<? extends E> c) {
    rangeCheckForAdd(index);

    Object[] a = c.toArray();
    int numNew = a.length;
    ensureCapacityInternal(size + numNew);  // Increments modCount

    int numMoved = size - index;
    if (numMoved > 0)
        // 原来的数据后移numNew位
        System.arraycopy(elementData, index, elementData, index + numNew,
                         numMoved);
    // 把新数据插入
    System.arraycopy(a, 0, elementData, index, numNew);
    size += numNew;
    return numNew != 0;
}
```

## 总结

ArrayList内部使用数组实现，初始容量是10，每次扩容怎加150%，最大容量是Integer.MAX_VALUE ，由于数组是连续的空间，所以查询和修改是很快的，但增加和删除要复制移动所有元素效率不如LinkedList.