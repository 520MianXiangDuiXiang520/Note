Life is not a ridiculous number of life, the meaning of life lies in life itself

<!-- more -->

# HashMap源码

## 散列集

数组和链表可以保持元素插入的顺序，对数组来说，他的优点是拥有连续的存储空间，因此可以使用元素下标快速访问，但缺点在于如果要在数组中第n位删除或插入一个新元素，就需要移动n后面的所有元素，比如在ArrayList中删除某个元素就是调用系统的arraycopy方法将数组要删除的元素后面的所有元素向前复制一位得到的。

```java
private void fastRemove(int index) {
    modCount++;
    int numMoved = size - index - 1;
    if (numMoved > 0)
        // 将elementData中从index + 1开始的numMoved长度的元素复制到elementData的index位置
        System.arraycopy(elementData, index+1, elementData, index,
                         numMoved);
    elementData[--size] = null; // clear to let GC do its work
}
```



并且定义数组时必须指定容量，如果需要扩容就得重新申请一个更大的数组，然后把原来的数据复制到新数组中，

这就导致数组查询很快，但增删性能不高。

而对链表来说，它的内存空间不是连续的，也就不需要考虑容量问题，但这就导致链表的查询需要逐个遍历LinkedList中虽然可以通过索引来get元素，但也是从头部开始遍历的（如果索引大于size/2就从尾部遍历），效率很低。

散列集（hash table）可以说是数组与链表的组合，

![UTOOLS1586163610224.png](http://yanxuan.nosdn.127.net/062609caebb2714e8b6b045d9826d75f.png)



往散列集中添加元素时，通过hash函数可以得到一个该元素的一个哈希值，Java中哈希值的范围在`-2147483648~2147483647`之间，Object类的`hashCode()`方法可以返回对象的哈希值，通过hashCode可以确定将该元素存到哪一个数组中，

> 不能直接使用hashCode,因为它的范围将近40亿，不可能有这么大的数组空间，所以需要对hashCode值做一定的处理，使之在数组容量范围内，最简单的办法是对数组容量取余，但取余有效率问题，所以Java使用了&操作，

如果key是null， 就返回0，否则返回原来哈希值与哈希值右移16位后的结果

比如一个元素的hashCode经过运算得到的值是5，他就会被放在第六个数组中。

应为数组容量是有限的，就一定存在运算后得到同样索引值的情况，称为哈希碰撞，解决哈希碰撞有两种方法：**开放地址法**和**拉链法** ，开放地址法是指如果当前的数组已经有元素了，就通过别的算法算出一个新位置插入，像python中dict的实现就使用了开放地址法；而Java中则使用了后者——拉链法，他的思路是如果当前位置有元素了，就把新元素链到旧元素上。

jdk 1.7 以及之前拉链使用一个链表实现，每次有冲突的新元素过来就会把新元素放到数组中，原来的旧链链接到新元素后面【头插法】；

jdk 1.8 开始加入了红黑树，如果数组某个位置的长度超过8并且数组容量超过32就会把链表转换为红黑树，如果红黑树经过删除节点数小于6，就会把树重新转换回链表，以此来提高效率。

## JDK 1.7 中的实现

jdk 1.7 以及之前那个数组是Entry类型的，里面封装了key和value,也就是链表的一个节点。

```java
static class Entry<K,V> implements Map.Entry<K,V> {
    final K key;
    V value;
    Entry<K,V> next;
    int hash;
}
```



### 基本属性

```java
// 数组的默认大小，必须是2的倍数， 默认16
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16

// 数组最大容量
static final int MAXIMUM_CAPACITY = 1 << 30;

// 默认负载因子，如果数组中75%被占满，就要扩容
static final float DEFAULT_LOAD_FACTOR = 0.75f;

// hashMap中数据的数量
transient int size;

// 与快速失败有关
transient int modCount;
```

### put方法

```java
public V put(K key, V value) {
    if (table == EMPTY_TABLE) {
        // 初始化一个数组
        inflateTable(threshold);
    }
    // key为null的情况
    if (key == null)
        return putForNullKey(value);
    // 正常其他情况
    int hash = hash(key);
    int i = indexFor(hash, table.length);
    for (Entry<K,V> e = table[i]; e != null; e = e.next) {
        Object k;
        if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
            V oldValue = e.value;
            e.value = value;
            e.recordAccess(this);
            return oldValue;
        }
    }

    modCount++;
    addEntry(hash, key, value, i);
    return null;
}
```

如果当前table是空的的时候（实例化后第一次执行put），需要通过`inflateTable()`对哈希表进行初始化

```java
private void inflateTable(int toSize) {
    // Find a power of 2 >= toSize
    // 计算实际的数组大小
    int capacity = roundUpToPowerOf2(toSize);

    // 计算出扩容的临界值threshold
    threshold = (int) Math.min(capacity * loadFactor, MAXIMUM_CAPACITY + 1);
    // 实例化一个新数组
    table = new Entry[capacity];
    initHashSeedAsNeeded(capacity);
}
```

由于数组容量要求是2的倍数，所以这个方法会先通过`roundUpToPowerOf2()`根据我们指定的数组容量计算出真实的数组容量capacity，然后实例化一个capacity大小的Entry数组。最后这个`initHashSeedAsNeeded()`允许你配置一个哈希种子，来手动影响散列结果。

```java
    private static int roundUpToPowerOf2(int number) {
        // assert number >= 0 : "number must be non-negative";
        return number >= MAXIMUM_CAPACITY
                ? MAXIMUM_CAPACITY
                : (number > 1) ? Integer.highestOneBit((number - 1) << 1) : 1;
    }
```



初始化后，由于HashMap允许null作为key值，所以如果key是null，就执行`putForNullKey()`方法把`null: value`存入哈希表.

```java
private V putForNullKey(V value) {
    // 遍历数组0位的链表
    for (Entry<K,V> e = table[0]; e != null; e = e.next) {
        // 如果数组0位链表某个节点key也是null，就替换该节点的值，返回旧值。
        if (e.key == null) {
            V oldValue = e.value;
            e.value = value;
            // 空方法
            e.recordAccess(this);
            return oldValue;
        }
    }
    // 如果0位没有key为null的节点，就创建新节点并加入链表
    modCount++;
    addEntry(0, null, value, 0);
    return null;
}
```

```java
void addEntry(int hash, K key, V value, int bucketIndex) {
    // 如果HashMap中元素的数量大于临界值并且发生了冲突，就扩容
    if ((size >= threshold) && (null != table[bucketIndex])) {
        resize(2 * table.length);
        hash = (null != key) ? hash(key) : 0;
        bucketIndex = indexFor(hash, table.length);
    }
    // 创建新的Entry对象
    createEntry(hash, key, value, bucketIndex);
}
```

```java
void createEntry(int hash, K key, V value, int bucketIndex) {
    // 原来的链表
    Entry<K,V> e = table[bucketIndex];
    // 实例化一个新的Entry对象，next指向旧的链表e
    table[bucketIndex] = new Entry<>(hash, key, value, e);
    // 元素个数加一
    size++;
}
```

> 1. HashMap允许null作为key，并且这个元素始终放在数组第0位

------

回到正常情况，key是null就确定它存放在数组0位，但其他的key就需要通过计算得到index值，jdk1.7中首先在`hash()`方法中对对象原本的hashCode做一系列移位操作后，再在`indexFor()`方法中与数组长度做与运算得出对象最终应该被放在数组的哪一位。

```java
final int hash(Object k) {
    // 可以设置环境变量来提供一个哈希种子
    int h = hashSeed;
    if (0 != h && k instanceof String) {
        return sun.misc.Hashing.stringHash32((String) k);
    }

    // 这个种子会通过与对象原来的hashCode做异或从而影响最终散列效果
    h ^= k.hashCode();

    h ^= (h >>> 20) ^ (h >>> 12);
    return h ^ (h >>> 7) ^ (h >>> 4);
}
```

```java
static int indexFor(int h, int length) {
    return h & (length-1);
}
```

出于性能的考虑，在获得最终的index时，Java采用了`&`操作而不是更简单的取余，这就导致数组长度必须是2的倍数，同时`hash()`方法中多次移位和异或也是应为这样。

> 比如一个字符串 “重地” 通过 `hashCode()`方法得到它原先的hashCode值为 1179395，假设数组没扩容，哈希种子是默认值0，那它计算index的过程应该是：
>
> 1. 与hashSeed做异或，得到的还是它本身
>
> 2. 右移20位的结果与右移12位的结果做异或
>
>    ```txt
>    h =         : 0000 0000 0001 0001 1111 1111 0000 0011 (1179395)
>    a = h >>> 20: 0000 0000 0000 0000 0000 0000 0000 0001 (1)
>    b = h >>> 12: 0000 0000 0000 0000 0000 0001 0001 1111‬ (287)
>    ----------------------------------------------------------------
>    a ^ b =     : 0000 0000 0000 0000 0000 0001 0001 1110 (286)
>    h =         : 0000 0000 0001 0001 1111 1111 0000 0011 (1179395)
>    ----------------------------------------------------------------
>    h =         : 0000 0000 0001 0001 1111 1110 0001 1101 (1179165)
>    c = h >>> 7 : 0000 0000 0000 0000 0010 0011 1111 1100
>    ----------------------------------------------------------------
>    h ^ c =     : 0000 0000 0001 0001 1101 1101 1110 0001
>    d = h >>> 4 : 0000 0000 0000 0001 0001 1101 1101 1110
>    ----------------------------------------------------------------
>    h ^ d =     : 0000 0000 0001 0000 1100 0000 0011 1111
>    len - 1     : 0000 0000 0000 0000 0000 0000 0000 1111
>    ----------------------------------------------------------------
>    index &     : 0000 0000 0000 0000 0000 0000 0000 1111
>    ```
>
>    到最后发现，真正参与运算的只有低四位，之所以做多次位移和异或运算，就是为了把hashCode的高位也参与到最后的与运算中，让得到的index尽量分散，如果把最高位用A表示，可以看到经过上面的算法，最高位究竟影响了哪些位置：
>
>    ```txt
>    h =         : A000 0000 0001 0001 1111 1111 0000 0011 (1179395)
>    a = h >>> 20: 0000 0000 0000 0000 000A 0000 0000 0001 (1)
>    b = h >>> 12: 0000 0000 0000 A000 0000 0001 0001 1111‬ (287)
>    ----------------------------------------------------------------
>    a ^ b =     : 0000 0000 0000 A000 000A 0001 0001 1110 (286)
>    h =         : 0000 0000 0001 0001 1111 1111 0000 0011 (1179395)
>    ----------------------------------------------------------------
>    h =         : 0000 0000 0001 A001 111A 1110 0001 1101 (1179165)
>    c = h >>> 7 : 0000 0000 0000 0000 001A 0011 11A1 1100
>    ----------------------------------------------------------------
>    h ^ c =     : 0000 0000 0001 A001 110A 1101 11A0 0001
>    d = h >>> 4 : 0000 0000 0000 0001 A001 110A 1101 11A0
>    ----------------------------------------------------------------
>    h ^ d =     : 0000 0000 0001 A000 110A 000A 00A1 11A1
>    len - 1     : 0000 0000 0000 0000 0000 0000 0000 1111
>    ----------------------------------------------------------------
>    index &     : 0000 0000 0000 A000 000A 000A 00A0 11A1
>    ```
>
>    最高位最后影响了低四位。
>
>    ##### 为什么数组容量要是2的倍数
>
>    让与运算之后的结果分布在 0 ~ (len -1) 之间

算出index之后的代码逻辑就和putForNullKey差不多了，唯一的区别在于：

```java
if (e.hash == hash && ((k = e.key) == key || key.equals(k))){...}
```

这样设计的原因在于：

* 哈希值不同一定不是同一个对象
* 同一个对象哈希值不一定相同

#### 扩容

是否扩容的判断在addEntry方法中，如果满足扩容条件，是先扩容，再添加新元素

```java
    void addEntry(int hash, K key, V value, int bucketIndex) {
        if ((size >= threshold) && (null != table[bucketIndex])) {
            // 2倍扩容
            resize(2 * table.length);
            hash = (null != key) ? hash(key) : 0;
            bucketIndex = indexFor(hash, table.length);
        }

        createEntry(hash, key, value, bucketIndex);
    }
```

扩容需要满足两个条件：

1. HashMap中**元素个数**大于等于threshold
2. 即将要新插入的元素发生了冲突

> 第一个条件 size是总元素个数，但threshold是根据数组容量算的。
>
> ```java
> threshold = (int) Math.min(capacity * loadFactor, MAXIMUM_CAPACITY + 1);
> ```

```java
void resize(int newCapacity) {
    // 得到旧数组的引用
    Entry[] oldTable = table;
    int oldCapacity = oldTable.length;
    // 如果旧数组已经不能再长了，就不扩容了
    if (oldCapacity == MAXIMUM_CAPACITY) {
        threshold = Integer.MAX_VALUE;
        return;
    }

    // 创建一个2倍旧数组大小的新数组
    Entry[] newTable = new Entry[newCapacity];
    // 将旧数组的元素转移到新数组
    transfer(newTable, initHashSeedAsNeeded(newCapacity));
    table = newTable;
    // 重新计算扩容临界值
    threshold = (int)Math.min(newCapacity * loadFactor, MAXIMUM_CAPACITY + 1);
}
```

扩容最核心的就是数据转移，也就是`transfer()`方法

```java
void transfer(Entry[] newTable, boolean rehash) {
    int newCapacity = newTable.length;
    // 第一重循环遍历数组
    for (Entry<K,V> e : table) {
        // 第二重循环遍历链表
        while(null != e) {
            Entry<K,V> next = e.next;
            if (rehash) {
                e.hash = null == e.key ? 0 : hash(e.key);
            }
            int i = indexFor(e.hash, newCapacity);
            // 到这又变成了尾插
            e.next = newTable[i];
            newTable[i] = e;
            e = next;
        }
    }
}
```

由于数组容量变了两倍，所以index也许需要重新计算，但计算中其实前面的步骤都一样，只不过最后一步时 length - 1 在最前面多了一个1，所以哪怕index值改变，变化后的index与原来的也是2的倍数关系（1.8中用到了这个规律）

##### 扩容过程中出现的循环链表的情况

![UTOOLS1586269660885.png](http://yanxuan.nosdn.127.net/a28177cb672a6c44f847d6fcd7d76e6d.png)

这是两个线程进入transfer后一开始的情况（两个线程现在都有了自己新的数组），如果线程1正常执行完成，线程2阻塞在`Entry<K,V> next = e.next;`之后，那结果就是：

![UTOOLS1586274296957.png](http://yanxuan.nosdn.127.net/1b0801f8011b6fd361badee0ac5437b3.png)

然后线程2开始执行

![UTOOLS1586274868757.png](http://yanxuan.nosdn.127.net/d9f52639ec643514b57a29a788808262.png)

就出现了循环链表的情况。

[参考](https://coolshell.cn/articles/9606.html)

[参考2](https://blog.csdn.net/weixin_42769637/article/details/103304102)

### get方法

get就很简单了

```java
public V get(Object key) {
    if (key == null)
        return getForNullKey();
    Entry<K,V> entry = getEntry(key);

    return null == entry ? null : entry.getValue();
}
```

```java
private V getForNullKey() {
    if (size == 0) {
        return null;
    }
    // null 是直接存在0位的
    for (Entry<K,V> e = table[0]; e != null; e = e.next) {
        if (e.key == null)
            return e.value;
    }
    return null;
}
```

```java
final Entry<K,V> getEntry(Object key) {
    if (size == 0) {
        return null;
    }

    int hash = (key == null) ? 0 : hash(key);
    for (Entry<K,V> e = table[indexFor(hash, table.length)];
         e != null;
         e = e.next) {
        Object k;
        if (e.hash == hash &&
            ((k = e.key) == key || (key != null && key.equals(k))))
            return e;
    }
    return null;
}
```

### remove方法

```java
public V remove(Object key) {
    Entry<K,V> e = removeEntryForKey(key);
    return (e == null ? null : e.value);
}
```

## JDK 1.8 的实现

jdk1.8 开始HashMap将解决冲突的办法改成了链表加红黑树，红黑树其实是一个自平衡的二叉查找树，所以如果数组某个位置链接了大量节点时，转变为红黑树会大幅提高查找效率，但红黑树的插入相对麻烦，所以只有在满足一定条件时才会把链表转换为红黑树。

### 基本属性

```java
// 数组的默认长度 16  
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16

// 数组的最大长度 2^30
static final int MAXIMUM_CAPACITY = 1 << 30;

// 默认的负载因子 0.75f
static final float DEFAULT_LOAD_FACTOR = 0.75f;

// 默认树化的链表临界长度 8
static final int TREEIFY_THRESHOLD = 8;

// 默认红黑树重新转换为链表时的临界节点数
static final int UNTREEIFY_THRESHOLD = 6;

// 默认将链表转换为树时最小的数组长度
static final int MIN_TREEIFY_CAPACITY = 64;

// 用于初始化数组
transient Node<K,V>[] table;

// 一个空的entrySet
transient Set<Map.Entry<K,V>> entrySet;

// 元素个数
transient int size;

// 用于快速失败
transient int modCount;

// 扩容阈值
int threshold;

// 负载因子
final float loadFactor;
```



### put方法

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

jdk1.8 中，put这个方法只是调用`hash()`重新求了一下对象的哈希值，剩余操作全部放在了`putVal()`中。

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

这里重新求哈希值的方法比1.7中简单了很多，也取消了哈希种子的设置，原因还是引入了红黑树后，哪怕发生大量冲突还是能保持较高的效率，所以就可以适当简化散列操作。右移16位后做异或还是为了让高位参与到最后求index的操作中，以此减缓冲突。

同样不变的是key位null的键值对还是会被存放在数组0位。



然后就是这个复杂的putVal方法，个人感觉1.8的代码可读性下降了不少。

```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    Node<K,V>[] tab; Node<K,V> p;
    int n, i;
    // 如果数组还没被实例化或长度为0，就初始化（扩容）
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    // 如果算出的数组index位没有元素就直接加入
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        // 这个e的作用是：如果put的key重复了，就把找到的重复的那个键值对象赋值给e，
        // 否则e就是null，说明key没有重复
        Node<K,V> e;
        K k;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        // 如果当前数组保存的树的话，就调用往树里插入元素的方法
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            // 开始遍历链表
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    // 遍历到最后发现没有重复的key，就把新节点插入到链表尾部
                    p.next = newNode(hash, key, value, null);
                    // 判断插入新节点后，有没有达到树化条件
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        // 树化
                        treeifyBin(tab, hash);
                    break;
                }
                // 找到了重复的key
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        // 处理重复的值
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

扩容

```java
final Node<K,V>[] resize() {
    // 原来的HashMap
    Node<K,V>[] oldTab = table;
    // 原来数组的容量
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    // 原来的扩容临界阈值
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) {
        // 如果数组到了最大容量，就不扩容
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        // 新容量是就容量的2倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                 oldCap >= DEFAULT_INITIAL_CAPACITY)
            // 2倍阈值（oldCap > 16）
            newThr = oldThr << 1; // double threshold
    }
    // 原来的数组为空（初始化）时，数组容量为阈值
    else if (oldThr > 0) // initial capacity was placed in threshold
        newCap = oldThr;
    // 如果指定阈值不大于0，就使用默认阈值16
    else {               // zero initial threshold signifies using defaults
        newCap = DEFAULT_INITIAL_CAPACITY;
        // 默认新的阈值为 16 * 0.75
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
    // 如果得出新阈值是0，通过新容量 * 加载因子 得出新阈值
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                  (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    // 移动旧容器里的数据到新容器
    @SuppressWarnings({"rawtypes","unchecked"})
    // 创建一个新容器
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    if (oldTab != null) {
        // 遍历旧容器中数组的每一位
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            // 如果数组这一位不为空
            if ((e = oldTab[j]) != null) {
                // 把原来数组这一位指向null，让这块空间被回收
                oldTab[j] = null;
                // 如果只有一个元素，就直接加入新容器
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;
                // 如果这一位存的是红黑树
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                // 如果是链表
                else { // preserve order
                    // 转到新数组中元素位置不变的时的头尾节点
                    Node<K,V> loHead = null, loTail = null;
                    // 转到新数组中元素位置加oldCap的时的头尾节点
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    // 移动index不需要变的链
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    // 移动需要变的链
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}

```

![UTOOLS1586498786726.png](http://yanxuan.nosdn.127.net/5685eac79bec2f0e32df79a67086fac6.png)![UTOOLS1586498805550.png](http://yanxuan.nosdn.127.net/19edeb02f245d679fa54cf16baf4aae0.png)

![UTOOLS1586498819007.png](http://yanxuan.nosdn.127.net/d25f811026e15da9906e66b02a158f12.png)



 

