# Java多态

## 绑定

所谓绑定就是把**方法的调用**和**方法主体**（方法所在的类）绑定起来，有两种绑定方式，前期绑定和后期绑定，前期绑定又叫做编译时绑定，后期绑定又叫做运行时绑定。

* 前期绑定：程序在**执行**之前就已经进行了绑定
* 后期绑定：在执行过程中，根据对象类型动态的进行绑定

Java中除了使用static，final定义的方法外，其余都是后期绑定（private方法是final）

对于引用，也有两种类型，即编译时类型和运行时类型。

* 编译时类型：声明该引用时是什么类型，他就是什么类型
* 运行时类型：实际赋给这个引用的是什么类型，他才是什么类型

## 多态

* 编译时多态：方法重载
* 运行时多态：通过继承实现

静态方法与类相关，不具有多态性

## 构造器与多态

* 构造器是静态的，不具有多态性

初始化原则：

1. 一切开始之前，把分配给对象的存储空间符位0
2. 静态的初始化率先执行（main之前）
3. 先初始化基类
4. 初始化语句优先构造器执行

```java
package Note.Chapter8_3;

class Meal{
    private Lettuce h = new Lettuce();
    Meal(){
        System.out.println("meal");
    }
}

class Bread{
    private Lettuce h = new Lettuce();
    Bread(){
        System.out.println("bread");
    }
}

class Cheese{

    Cheese(){
        System.out.println("Cheese");
    }
}

class Lettuce{
    Lettuce(){
        System.out.println("Lettuce");
    }
}

class Lunch extends Meal{
    private static Lettuce h = new Lettuce();
    Lunch(){
        System.out.println("lunch");
    }
}

class ProTableLunch extends Lunch{
    ProTableLunch(){
        System.out.println("protablelunch");
    }
}

public class Sandwich extends ProTableLunch {
    private static Bread bb = new Bread();
    private Bread b = new Bread();
    private Cheese c = new Cheese();
    private Lettuce l = new Lettuce();
    public Sandwich(){
        System.out.println("sandwich");
    }

    public static void main(String[] args) {
        System.out.println("main");
        new Sandwich();
    }
}

//Lettuce
//Lettuce
//bread
//main
//Lettuce
//meal
//lunch
//protablelunch
//Lettuce
//bread
//Cheese
//Lettuce
//sandwich
```

## 构造器内部的多态

在构造器内部调用正在构造的对象的某个动态绑定的方法


