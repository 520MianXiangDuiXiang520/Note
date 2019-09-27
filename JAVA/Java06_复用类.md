# 复用类

Java复用类有两种方法，组合和继承

## 组合

### 什么是组合

在一个类中引用另一个类的对象

### 引用什么时候初始化

类中域为基本数据类型时，会被赋初值为0，对象的引用则会被赋值为null，调用它的任何方法都会抛出异常，但如果打印它，会得到null

* 创建引用时
* 在构造器中
* 惰性初始化（使用时）

```java
package Note;
import static junbao.tool.Print.*;

class Demo {
    private String s;
    Demo(String name){
        s = name;
        coutln("new Demo object" + s);
    }
    public String toString(){
        return s;
    }
}

public class Chapter7_1 {
    // 定义时初始化
    private Demo demo = new Demo("demo");
    private Demo demo2, demo3;

    Chapter7_1(){
        // 构造器中初始化
        demo2 = new Demo("demo2");
    }

    public String toString(){
        if (demo3 == null){
            demo3 = new Demo("demo3");
        }
        return "demo3:" + demo3 + "  demo2" + demo2 + "  demo" + demo;
    }

    public static void main(String[] args) {
        Chapter7_1 c = new Chapter7_1();
        coutln(c);
    }
}

```

toString方法：每一个非基本数据类型对象都有一个toString方法，当编译器需要一个String而你只有一个object时，会自动调用该方法。
