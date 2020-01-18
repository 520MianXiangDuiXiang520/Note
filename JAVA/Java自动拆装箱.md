---
title: "java 自动装拆箱"
tags: 
  - Java
---

将基本数据类型封装成对象的过程叫做装箱（boxing），反之基本数据类型对应的包装类转换为基本数据类型的过程叫做拆箱（unboxing）;

<!-- more -->

## 基本数据类型与其他对象的区别

### 基本数据类型

Java是一门面向对象的强类型语言，但它又不像python那样一切皆对象，Java中有一部分使用最频繁的数据结构并不是面向对象的，他们就是基本数据类型，也叫内置类型，他们在栈中储存，比起其他用`new`创建的对象，更加高效，Java有9中基本数据类型，分为五类

|类型|标识符|备注|
|----|-----|----|
|整型|byte, short, int, long||
|浮点|float, dauble||
|字符|char||
|布尔|boolean||
|空|void|不能操作|

#### 基本数据类型的范围

整型的范围

* byte： 占一个字节，也就是8位，最高一位作为符号位，有效位只有7位（采用补码存储）。

```txt
最大值：0，111 1111（127）
最小值：1，000 0000（-128）
```
> 怎么算的？
> 最高一位是符号位，这是固定的，正数用0表示，负数用1表示，然后后面的七位最大是7个1，最小是7个0，这就是用补码表示的byte能表示的最大最小数，把补码转换为原码（正数的补码就是源码，负数的补码变源码取反加一）然后转换为10进制。

* short：占两个字节，16位，有效15位

```txt
最大值：2^15 -1: 32,767
最小值：-(2^15): -32,768
```

* int: 占4个字节，最大值【2^31 - 1】(2,147,483,647), 最小值【-2^31】(-2,147,483,648)
* long: 占8字节，最大值【2^63 - 1】(9,223,372,036,854,775,807)，最小值【-2^63】(-9,223,372,036,854,775,808)

## 包装类型

Java中其他的对象都是继承自object的，有自己的属性和方法，为了方便基本基本数据类型和其他对象的的操作，Java为每个基本数据类型提供了对应的包装类型，

|基本数据类型|	包装类|
|-----|-----|
|byte|	Byte|
|boolean|	Boolean|
|short|	Short|
|char	|Character|
|int	|Integer|
|long	|Long|
|float	|Float|
|double	|Double|

* 为什么要使用包装类型

Java是一门面向对象的语言，大部分操作都是针对对象的，比如容器，容器中能存入的最大的范围就是object，而基本数据类型不属于对象，那他就无法存入容器，为了解决这个问题，必须把基本数据类型“包装”起来，让他作为一个对象参与到编程中。

## 装箱和拆箱

把基本数据类型包装成对象的过程叫做装箱，反之把对象转换为基本数据类型的过程叫做拆箱。  
Java SE5 后，为了简化开发，提供了自动装拆箱机制，Java会在适当时刻自动转换基本数据类型和包装类型，如：

```java
public class Demo1 {
    public static void main(String[] args) {
        Integer integer = 3; // 自动装箱
        int i = integer;  // 自动拆箱
    }
}
```

通过Javap反编译得到

```doc
  public static void main(java.lang.String[]);
    Code:
       0: iconst_3
       1: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
       4: astore_1
       5: aload_1
       6: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
       9: istore_2
      10: return
```

在自动装箱时，其实是调用了包装类的`valueOf()`方法，而在自动拆箱时则调用了包装类的`intValue()`方法，所以如果在JavaSE5之前，没有自动装拆箱机制，上面的代码我们需要这样写

```java
public class Demo1 {
    public static void main(String[] args) {
        Integer integer = Integer.valueOf(3); // 装箱
        int i = Integer.intValue(integer);  // 拆箱
    }
}
```

除int和Integer之外,其他基本类型和包装类的自动转换也一样，装箱时调用`valueOf()`方法，拆箱时调用`xxxValue()`方法。

### 什么时候自动装箱

#### 1. 初始化，赋值，函数返回时

当把基本数据类型赋值给包装类时或者基本数据类型作为函数返回值但函数声明要求返回包装类型时，会自动装箱，如上面的例子

#### 2. 将基本数据类型放入容器中

```java
public void func2(){
        List<Integer> list = new ArrayList<>();
        list.add(1);
    }
```

反汇编之后

```txt
  public void func2();
    Code:
       0: new           #4                  // class java/util/ArrayList
       3: dup
       4: invokespecial #5                  // Method java/util/ArrayList."<init>":()V
       7: astore_1
       8: aload_1
       9: iconst_1
      10: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      13: invokeinterface #6,  2            // InterfaceMethod java/util/List.add:(Ljava/lang/Object;)Z
      18: pop
      19: return
```

在第10步，使用了自动装箱



### 什么时候自动拆箱

#### 1. 初始化，赋值，函数返回时

把包装类对象赋值给基本数据类型的变量时，会自动拆箱（函数返回值原理一样）

#### 2. 包装类型做算数运算时

算数运算（包括比较大小）是针对基本数据类型的，所以无论是基本数据类型与包装类型还是包装类型与包装类型之间做运算都会转换成两个基本数据类型

```java
public void func3(){
        Integer integer = 3;
        int i = 1;
        Integer integer1 = 1;
        boolean b1 = integer > i; // 基本数据类型与包装类型比较大小
        boolean b2 = integer > integer1; // 两个包装类型比较大小
    }
```

反汇编后

```txt
public void func3();
    Code:
       0: iconst_3
       1: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
       4: astore_1
       5: iconst_1
       6: istore_2
       7: iconst_1
       8: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      11: astore_3
      12: aload_1
      13: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      16: iload_2
      17: if_icmple     24
      20: iconst_1
      21: goto          25
      24: iconst_0
      25: istore        4
      27: aload_1
      28: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      31: aload_3
      32: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      35: if_icmple     42
      38: iconst_1
      39: goto          43
      42: iconst_0
      43: istore        5
      45: return
```

通过13步，说明基本数据类型与包装类型比较大小会转换为两个基本数据类型再比较  
通过28，32步，说明两个包装类型比较大小也会转换为基本数据类型

普通的加减乘除也一样

```java
public void func4() {
        Integer integer = 3;
        int i = 1;
        Integer integer1 = 1;
        int s = integer + integer1;
        int s1 = integer + i;
    }
```

```txt
public void func4();
    Code:
      //...
      13: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      16: aload_3
      17: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      20: iadd
      21: istore        4
      23: aload_1
      24: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      //...
```

#### 3. 三目运算

如果三目运算的第二三位一个是基本数据类型另一个是包装类型时，会自动拆箱成两个基本数据类型

```java
public void func5() {
    boolean flag = true;
    Integer i = 8;
    int j;
    j = 3;
    int k = flag ? i: j;
}
```

```txt
  public void func5();
    Code:
       0: iconst_1
       1: istore_1
       2: bipush        8
       4: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
       7: astore_2
       8: iconst_3
       9: istore_3
      10: iload_1
      11: ifeq          21
      14: aload_2
      15: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      18: goto          22
      21: iload_3
      22: istore        4
      24: return
```

因为i是包装类型，j是基本数据类型，所以在14行把i自动拆箱成了基本数据类型（并不是应为三目运算返回的是int），所以做三目运算时应该注意，尤其是基本数据类型和对象混杂时，如果对象没被赋值，可能导致NPL（空指针异常）

> 只有一个是基本数据类型，一个是包装类对象时才会自动拆箱，两个对象是不拆的。

## 装箱和拆箱时的缓存问题

```java
public class Demo2 {
    public static void main(String[] args) {
        Integer a1 = 1;
        Integer a2 = 1;
        int a3 = 1;
        System.out.println(a1 == a2);  // true
        System.out.println(a1.equals(a2));  // true
        System.out.println(a1 == a3);  // true
        System.out.println(a1.equals(a3));  // true
    }
}
```

```java
public class Demo2 {
    public static void main(String[] args) {
        Integer a1 = 133;
        Integer a2 = 133;
        int a3 = 133;
        boolean b1 = a1 == a2;
        boolean b2 = a1.equals(a2);
        boolean b3 = a1 == a3;
        boolean b4 = a1.equals(a3);
        System.out.println(b1);  // false
        System.out.println(b2);  // true
        System.out.println(b3);  // true
        System.out.println(b4);  // true
    }
}
```

两次结果不同，原因就是自动拆装箱时存在缓存问题，当我们第一次使用Integer时，Java会初始化一个`Integer[] cache`然后通过循环把-128到127之间的数加入到这个缓存中，如果新new的Integer的值在这个范围内，就直接返回这个创建好的对象，`equals()`比较值，`==`比较是不是同一对象，所以不管怎样，equals的结果都是true,而`==`在-128 到 127 之间是true，超出这个范围是false。

> 这个就类似于python中的小整数池，但python的范围是[-5, 256]

除[-128, 127]之间的整数外，boolean的两个值，以及`\u0000`至 `\u007f`之间的字符也在常量池中。

## 总结

1. 什么是包装类

为了方便操作基本数据类型，对每一种基本类型提供一个包装类，他们将基本数据类型包装成一个对象

1. 什么是装箱，拆箱

把基本数据类型包装成包装类的过程叫装箱（使用包装类的`valueOf()方法`）  
把包装类转换为基本数据类型的过程叫拆箱（使用包装类的`xxxValue()方法`）

3. 什么是自动装箱/拆箱

Java SE5 引入的一种在特定情况下将基本数据类型自动转换为包装类/包装类自动转换为基本数据类型 的机制

4. 什么时候自动装箱
  1. `Integer a = 5`
  2. 函数返回值
  3. 把基本数据类型加入容器时

5. 什么时候自动拆箱
  1. 初始化，赋值， 函数返回值
  2. 三目运算第二第三个参数既有包装类，也有基本数据类型时
  3. 算术运算，比较大小

6. 什么是自动拆装箱时的缓存

第一次使用某些包装类时，Java会创建一个缓存池，以后每次需要包装类对象，就先会找缓存池中有没有，有就直接返回，没有才创建。缓存池的范围：

整型：[-128, 127]  
布尔：[true, false]  
字符：[`\u0000`, `\u007f`]

## 参考

[什么是Java中的自动拆装箱](https://blog.csdn.net/wufaliang003/article/details/82347077)  
[Java中整型的缓存机制](https://mp.weixin.qq.com/s?__biz=MzI3NzE0NjcwMg==&mid=402060056&idx=1&sn=1cd47760783b32b30e659398d36b233b&scene=21#wechat_redirect)



