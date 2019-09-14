# JAVA 操作符

## ==和equals

对于非基本数据类型，`==`比较的是对象的引用，若要比较对象内容是否相等需要使用`equals()`，但`equals()`默认行为也是比较引用，对于自定义的对象，需要在新类中覆盖`equals()`方法

## 直接常量

```java
public class Chapter3_9 {
    public static void main(String[] args) {
        // 直接常量
        int x1 = 0x2f;
        System.out.println("x1:" + x1 + " 二进制：" + Integer.toBinaryString(x1));
        int x2 = 0177;
        System.out.println("x2:" + x2 + " 二进制：" + Integer.toBinaryString(x2));
        char x3 = 0xffff;
        System.out.println("x3:" + x3 + " 二进制：" + Integer.toBinaryString(x3));
        byte x4 = 0x7f;
        System.out.println("x4:" + x4 + " 二进制：" + Integer.toBinaryString(x4));
        short x5 = 0x7fff;
        System.out.println("x5:" + x5 + " 二进制：" + Integer.toBinaryString(x5));

        long n1 = 200;
        long n2 = 200L;
        System.out.println("n1: " + n1);
        System.out.println("n2：" + n2);
    }
}
```

## 按位操作和移位操作

## 三元操作符

```java
i< 10? 1*100: i*10;>
```

## 类型转换

浮点数转换为int时，会对末尾进行截断，要进行舍入，需要使用`round()`
