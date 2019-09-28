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

## 继承

* 超类super:用来调用基类版本的方法
* 基类构造器的初始化：super(),必须作为导出类构造器的第一条语句
* 名称屏蔽：允许导出类重载或覆盖基类方法，有时覆盖可能会不小心成了重载，可以使用标签`@Override`声明覆盖，如果重载了就会抛出异常
* protected:受保护类型，包含包访问权限，对导出类表现为public，对用户表现为private
* 向上转型：导出类可以自动转型为基类类型

```java
package Note;
import static junbao.tool.Print.*;

class Father{
    private String name;

    Father(String name){
        this.name = name;
    }

    public void func1(){
        coutln("func1()");
    }

    public void func1(int s){
        coutln("func1(int)");
    }

    protected void func2(Father f){
        coutln("向上转型");
    }
}

public class Chapter7_2 extends Father {
    Chapter7_2(){
        super("son");
    }
    // 如果想覆盖，但不小心写成了重载，使用@Override注解就会报错
    @Override
    public void func1(){
        coutln("覆盖func1()");
    }
    public void func(){
        super.func1();
        func2(new Chapter7_2());
    }

    public static void main(String[] args) {
        Chapter7_2 c = new Chapter7_2();
        c.func1();
        c.func1(2);
        c.func();
    }
}

//覆盖func1()
//func1(int)
//func1()
//向上转型
```

### final的使用

用在三处：数据，方法，类

#### 对数据使用final

* 常量：必须是基本数据类型，用final表示，定义时必须赋值
* 一个即是ststic又是final的域占据一段不能改变的存储空间，大写，下划线分割
* 对对象的引用使用final时，引用只能指向初始化时的对象，不能改变指向，但对象可变
* 允许空白final，会被自动初始化（基本数据类型为0，引用为null），可以根据不同对象具有不同值
* 如果方法参数使用了final，则只能使用，不能修改，用于在匿名内部类传递参数

#### 方法使用final

* 作用：锁定方法，以防止继承类修改方法；提高效率（内嵌调用【新版本被劝阻使用】）
* final与private：private方法隐式被指定为final

#### 对类使用final

* final类不允许有别的类继承它

### 继承中初始化及类的加载

原则：

1. static优先
2. 基类优先
3. 变量初始化提前

初始化顺序：

1. 基类中的static变量初始化
2. 导出类的static变量初始化
3. main()
4. 基类普通变量初始化
5. 基类构造器
6. 导出类普通变量初始化
7. 导出类构造器
8. 方法执行

```java
package Note;
import static junbao.tool.Print.*;

class Insect{
    private int i = 9;
    protected int j = 0;
    Insect(){
        coutln("Insect i = " + i + " j = " + j);
        j = 39;
    }
    private static int x1 = printInit("static x1 init");
    private int x3 = printInit("base class no static");
    static int printInit(String s){
        coutln(s);
        return 47;
    }
}

public class Chapter7_9 extends Insect{
    private int k = printInit("Chapter7_9 k init");
    public Chapter7_9(){
        coutln("k = " + k);
        coutln("j = " + j);
    }
    private static int x2 = printInit("Chapter7_9 static x2 init ");

    public static void main(String[] args) {
        coutln("main()");
        Chapter7_9 c = new Chapter7_9();
    }
}

// static x1 init
// Chapter7_9 static x2 init
// main()
// Insert i = 9 j = 39
// Chapter7_9 k init
// k = 47
// j = 39
```

## 代理

处于组合和继承之间的中庸之道，Java并不直接支持，但大部分IDE支持，将成员对象置于要构造的类中

```java
package Note;
import static junbao.tool.Print.*;

class Proxy{
    protected void run(String s){
        coutln("run()");
    }
    protected void jump(){
        coutln("jump()");
    }
}

public class Chapter7_5 {
    private Proxy proxy;
    Chapter7_5(){
        proxy = new Proxy();
    }
    public void run(String s){
        proxy.run(s);
    }
    public void jump(){
        proxy.jump();
    }
}

```

## 总结

组合是将现有类型作为新类型底层实现的一部分  
继承是复用了基类的接口，所以能向上转型  
