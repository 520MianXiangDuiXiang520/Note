# Lambda表达式

jdk 1.8 新加入的特性，简化了简单接口的实现

## 函数式接口

函数式中只有一个待实现的方法，可以使用`@FunctionalInterface`注解标注函数式接口.这个接口中只能有一个待实现的方法，但可以包含默认方法，静态方法以及Object类中的public方法

```java
package Note.lambda_demo;

@FunctionalInterface
public interface Demo01 {
    void test();

    default void defMethod() {
        System.out.println("default function");
    }

    static void staticMethod() {
        System.out.println("static function");
    }

    @Override
    boolean equals(Object object);
}

```

## Lambda表达式的使用

在1.8之前，如果想要使用这样的接口，通常可以使用匿名内部类实现，

```java
Demo01 demo01 = new Demo01() {
            @Override
            public void test() {
                System.out.println("通过匿名内部类实现接口");
            }
        };
```

但现在可以更简单的使用

```java
Demo01 demo01 = () -> {
    System.out.println("demo01");
};
```

lambda 的标准格式：

```java
(args) -> {};
```

* 没有参数括号中留白

* 如果方法体只有一条语句，可以省略`{}`,如：

  ```java
  Demo01 demo01 = () -> System.out.println("lll");
  ```

* 如果方法体只有一条return语句，可以简写，如：

  ```java
  Demo02 demo02 = (int s) -> s * s;
  
  // 等效于
  
  Demo02 demo02 = (int s) -> {return s * s};
  ```

* 如果方法体只返回一个新实例，可以简写为：

  ```java
  Demo04 demo04 = HashMap::new;
  
  // 等效于
  
  Demo04 demo04 = () -> new HashMap();
  ```

  

## 自带函数接口

java.util.function 包下提供了很多内置的函数式接口，常用的有`Predicate<T>`、`Consumer<T>`，以及`Function<T, R>`，

### Predicate

用来判断传入的值是否符合条件

```java
@FunctionalInterface
public interface Predicate<T> {
    boolean test(T t);
    // ...
}
```

示例：

```java
// 用来找出数组中的偶数
package Note.lambda_demo;

import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.function.Predicate;

public class Main {
    public Object[] filterInteger(int[] nums, Predicate<Integer> filter) {
        LinkedList<Integer> result = new LinkedList<Integer>();
        for (int i = 0; i < nums.length; i++) {
            if(filter.test(nums[i])){
                result.add(nums[i]);
            }
        }
        return result.toArray();
    }
    
    public static void main(String[] args) {
        Predicate<Integer> predicate = (Integer s) -> s % 2 == 0;
        int [] nums = {-1, 2, 8, -9, 0, 7, -5};
        Main main = new Main();
        System.out.println(Arrays.toString(main.filterInteger(nums, predicate)));

    }
}//~ [2, 8, 0]

```

### Consumer

表示输入单个参数，返回某个值的操作

```java
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
}
```

### Function

```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}
```

代表一类函数，这类函数接收一个T类型的参数，返回一个R类型的结果

## 其他

* lambda表达式中可以省略参数类型

* lambda表达式中可以使用实例变量、静态变量，以及局部变量

* 如果两个函数式接口类似，可以简写，如：

  ```java
  package Note.lambda_demo;
  
  @FunctionalInterface
  public interface Demo02 {
      int test(int a);
  }
  
  // 又有一个类似的接口Demo03
  package Note.lambda_demo;
  
  @FunctionalInterface
  public interface Demo03 {
      int test(int s);
  }
  ```

  使用时，可以用`::`简写

  ```java
  Demo02 demo02 = (int s) -> s * s;
  
  demo01.test();
  System.out.println(demo02.test(13));
  
  Demo03 demo03 = demo02::test;
  System.out.println(demo03.test(10));
  ```

  