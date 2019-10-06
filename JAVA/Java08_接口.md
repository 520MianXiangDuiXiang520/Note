# Java 接口

## 抽象类

含有抽象方法的类就是抽象类，抽象方法使用`abstract`定义，只有声明，没有实现，也可以直接使用`abstract`声明抽象类，抽象类中可以有零个或多个抽象方法。  
抽象类不允许有实例化对象，否则在编期就会报错。

## 接口

使用`interface` 替换类声明时的 `class` 声明接口，接口中的方法只有声明，没有实现，并且默认为public，接口中可以拥有域，但会被默认为`static final`

### 接口的实现

使用`implements`替换继承时的`extends` 来实现一个接口，接口实现必须覆盖接口中的所有方法声明，并且必须为public

### 完全解耦

* 策略模式： 定义一个方法，根据传递的参数的不同，表现出不同的行为
* 适配器模式： 接受所拥有的接口，产生所需要的接口

### 多重继承

Java不允许类多重继承，但允许接口多重继承，并且可以向上转型为所有接口

接口也可以继承以拓展接口，使用`extends`可以继承多个接口

### 适配接口

定义接受接口作为参数的方法，只要对象遵循接口，就可以调用这个方法。

### 接口与工厂

* 工厂方法模式：定义一个工厂方法，这个方法用来生产接口的某个实现的对象。

```java
package Note.Chapter9_9;
import static junbao.tool.Print.*;

interface Cycle {
    String name();
    int wheel_num();
}

interface CycleFactor{
    Cycle getCycle();
}

class Unicycle implements Cycle{
    @Override
    public String name() {
        return "独轮车";
    }

    @Override
    public int wheel_num() {
        return 1;
    }
}

class UnicycleFactor implements CycleFactor{
    @Override
    public Cycle getCycle() {
        return new Unicycle();
    }
}

class Bicycle implements Cycle{
    @Override
    public String name() {
        return "自行车";
    }

    @Override
    public int wheel_num() {
        return 2;
    }
}

class BicycleFactor implements CycleFactor{
    @Override
    public Cycle getCycle() {
        return new Bicycle();
    }
}

class Tricycle implements Cycle{
    @Override
    public String name() {
        return "三轮车";
    }

    @Override
    public int wheel_num() {
        return 3;
    }
}

class TricycleFactor implements CycleFactor{
    @Override
    public Cycle getCycle() {
        return new Tricycle();
    }
}

public class Cycles{
    public static void theCycle(CycleFactor cycleFactor){
        // 这里如果是特别复杂的代码，需要有多个Cycle的实例
        Cycle cycle = cycleFactor.getCycle();
        coutln(cycle.name() + "有" + cycle.wheel_num() + "个轮子");
    }
    public static void withoutFactor(Cycle cycle){
        coutln(cycle.name() + "有" + cycle.wheel_num() + "个轮子");
    }

    public static void main(String[] args) {
        theCycle(new UnicycleFactor());
        theCycle(new BicycleFactor());
        theCycle(new TricycleFactor());
        // 单例模式，之所以不直接传递接口的实现的对象，应为这样在theCycle中就只有一个对象了，
        // 有时候需要实例化很多次，所以传递工厂对象是最佳的选择
        withoutFactor(new Tricycle());
    }
}
```

## 总结

接口是一种很重要的工具，但容易滥用，原则上应该优先选择类而不是接口，如果接口的必要性变得非常明确，那么就应该进行重构。




















