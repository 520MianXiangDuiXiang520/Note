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

### 构造器与多态

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

### 构造器内部的多态

在构造器内部调用正在构造的对象的某个动态绑定的方法

## 协变返回类型

Java SE5 中加入  
条件：

1. 有两个类AB，导出类B覆盖了基类A的某个方法process
2. A.process返回类C的一个实例

结果：  

允许B.process 返回C的导出类的实例

## 用继承进行设计

原则：优先使用组合

### 状态模式

根据属性的变化改变对象的行为

```java
package exercise.exercise8_5;
import static junbao.tool.Print.*;

class StarShip{
    public void ship(){}
}

class DangerStarShip extends StarShip{
    public void ship(){
        coutln("DANGER StarShip");
    }
}

class NervousStarShip extends StarShip{
    public void ship(){
        coutln("NERVOUS StarShip");
    }
}

class PeaceStarShip extends StarShip{
    public void ship(){
        coutln("PEACE StarShip");
    }
}

class Space{
    private StarShip alertStatus = new PeaceStarShip();
    private int danger_level = -1;
    private void changeDanger(){
        if(danger_level  == 0){
            alertStatus = new NervousStarShip();
        }
        else if (danger_level < 0){
            alertStatus = new PeaceStarShip();
        }
        else {
            alertStatus = new DangerStarShip();
        }
    }
    public void addDanger(){
        danger_level ++;
        changeDanger();
    }
    public void subtractDanger(){
        danger_level --;
        changeDanger();
    }
    public void fly(){
        alertStatus.ship();
    }

}

public class Transmogrify {
    public static void main(String[] args) {
        Space s = new Space();
        s.fly();
        s.addDanger();
        s.fly();
        s.addDanger();
        s.fly();
        s.subtractDanger();
        s.fly();
    }
}

```

### 纯继承与拓展

如果导出类与基类有相同的接口，即导出类没有拓展基类接口，这就是“is-a”（是一种）的关系，向上转型没有任何问题，但如果导出类拓展了基类接口（大多数情况下），向上转型后这些拓展的方法就无法访问了，这时就需要用到向下转型，在Java中，所有的转型都会接受检查，以确保它的确是我们所希望的那种类型，如果不是就会抛出ClassCastException异常，这种检查叫做RTTI（运行时类型检查）

```java
class Father{
    public void a(){}
}

class Son extends Father{
    public void a(){}
    public void b(){}
}

public class Main{
    public static void main(String[] args) {
        Father [] f = {
                new Father(),
                new Son()
        };
        f[0].a();
        f[1].a();
//        f[0].b();
//        f[1].b();
//        ((Son)f[0]).b();  // Exception in thread "main" java.lang.ClassCastException:
        ((Son)f[1]).b();
    }
}
```
