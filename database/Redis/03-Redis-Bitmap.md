# Redis-Bitmap

BitMap,即位图，是一个byte数组，用二进制表示，只能存储0和1，BitMap并不是一个特殊的数据结构，它实质上还是普通的字符串。

<!-- more -->

## 1. 操作API

由于BitMap本质上还是String, 所以我们可以使用`get/set`直接获取整个位图的内容，也可以使用提供的专门的`getbit/setbit`来按位处理



| 命令                | 含义                       |
| ------------------- | -------------------------- |
| `getbit key offset` | 获取指定偏移量offset上的位 |
|`setbit key offset value` | 设置指定偏移量上的位，返回该位之前的值，value只能取0和1|
|`bitcount key [start end]`| 获取指定范围中值为1的个数 |
|`BITOP AND destkey key[ key1...]`| 对一个或多个 key 求逻辑并，并将结果保存到destkey（AND也可以是`OR(或)`, `NOT(非)`, `XOR(异或)`）；**如果处理的字符串长度不一致，短的那个字符串缺下的会以0填充** |
|`BITPOS key tartgetBit [start end]`| 返回指定范围内第一个值等于tartgetBit的值的偏移量，找不到返回-1，targetBit只能取0和1|

## 2. 应用场景



### 2.1 统计日活跃用户

* key: 日期
* offset: 用户ID
* value：是否活跃

### 2.2 签到记录

* key：用户ID
* offset: 日期
* value：是否签到

### 2.3 统计在线人数

* key： 可以是某个在线状态或日期
* offset: 用户ID
* value： 是否在线