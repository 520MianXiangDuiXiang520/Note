# 设计模式

> 参考：
>
> * 《大话设计模式》
> * [菜鸟教程|设计模式简介](https://www.runoob.com/design-pattern/design-pattern-intro.html)

## 设计模式的六大原则 

> 参考：
>
> * [设计模式六大原则](http://www.uml.org.cn/sjms/201211023.asp#6)

### 1. 单一职责原则

一个类只负责一个明确的功能 

**优点：**

* 降低类的复杂度，提高代码可读性和可维护性
* 降低变更时对其他功能的影响

### 2. 里氏替换原则

**原则一：**若 o1 是 C1 的一个实例化对象， o2 是 C2 的一个实例化对象，如果在使用 C1 的程序中将o1 替换为 o2 而程序行为没有发生变化，那么 C2 应该是 C1 的子类。

**原则二：**所有用到基类对象的地方，如果把基类对象替换成子类对象，程序行为不应该发生变化。

**实现方法：**

1. 子类可以实现父类的抽象方法，但不能覆盖父类的非抽象方法；
2. 允许子类拓展父类的方法
3. 当子类的方法重载父类的方法时，方法的前置条件（即方法的形参）要比父类方法的输入参数更宽松。
4. 当子类的方法实现父类的抽象方法时，方法的后置条件（即方法的返回值）要比父类更严格。

### 3. 依赖倒置原则

> 高层模块不应该依赖低层模块，二者都应该依赖其抽象；抽象不应该依赖细节；细节应该依赖抽象。

比如手机（Phone）依赖CPU，那么 Phone 就是一个高层模块， CPU 就是一的低层模块，Phone 显然不应该依赖一个具体的低层模块（如 Qualcomm865）：

```java
public class Phone {
    private Qualcomm cpu;

    Phone(){
        this.cpu = new Qualcomm();
    }

    public void printConfig(){
        System.out.println("cpu is" + this.cpu);
    }
}
```

不管是高通还是麒麟，都应该抽象为一个CPU类，然后各自实现，高层模块只依赖于抽象的低层模块。

**实现方法：**

1. 低层模块尽量都要有抽象类或接口，或者两者都有。
2. 变量的声明类型尽量是抽象类或接口。
3. 使用继承时遵循里氏替换原则。

### 4. 接口隔离原则

> 客户端不应该依赖它不需要的接口；一个类对另一个类的依赖应该建立在最小的接口上。
>
> 使用多个隔离的接口，比使用单个接口要好.

[接口隔离原则](http://www.uml.org.cn/sjms/201211023.asp#6)

### 5. 迪米特法则

> 一个对象应该对其他对象保持最少的了解。

高内聚，低耦合

### 6. 开闭原则

**对拓展开放，对修改封闭**：当系统变化时，尽量通过拓展来实现变化，而不是去修改原有代码；

## 简单工厂模式

> 2020 / 4 / 30 
>
> 参考：
>
> * [CSDN|简单工厂模式](https://blog.csdn.net/xingjiarong/article/details/49999121)

简单工厂通过传给工厂类的参数的不同，返回不同的对象，包括三部分组成：

1. 具体的”产品“
2. 工厂类（实例化并返回”产品“）
3. 客户端（使用”产品“）

### 为什么使用简单工厂：

1. ”产品“的创建过程可能很复杂，涉及到多个不同类之间的依赖，通过简单工厂将创建过程隐藏在工厂类中，一方面减轻了客户端使用该产品的难度，另一方面也防止了客户端错误创建产品造成的安全问题。
2. 将产品的生产和消费过程分离开，这样如果要有了一个新的产品，只需要把它加入到工厂类中，客户端需要时工厂类就会返回给它，否则的话，每次添加一个新的产品，都需要修改客户端代码，违反开闭原则。

### 简单工厂的缺点：

1. 系统过度依赖工厂类，工厂类作为一个”上帝类“，负责创建客户端需要的所有对象，导致一旦工厂类出错，整个系统就会崩溃。
2. 如果”产品类“特别多，工厂类中就会有很多个分支，造成工厂类异常庞大，难以维护。
3. 每次添加新的产品都要修改工厂类，从工厂类的角度看违反了”开闭原则“，也不利于系统拓展。
4. 工厂方法一般是静态方法，不利于继承。

### 适用场景

1. 工厂类负责创建的对象比较少：由于创建的对象较少，不会造成工厂方法中的业务逻辑太过复杂。

2. 客户端只知道传入工厂类的参数，对于如何创建对象不关心：客户端既不需要关心创建细节，甚至连类名都不需要记住，只需要知道类型所对应的参数。

### 例：

如果需要获取不同的手机对象，就可以使用简单工厂，具体的手机对象依赖于CPU， Camera等，通过简单工厂的封装，客户端获取 Phone 对象时就不需要了解具体的 ”生产过程“了.

> 实例化CPU， Camera 等配件时，也应该使用简单工厂。

<img src="http://yanxuan.nosdn.127.net/8c2d7b05901a76b4c9b1bef5f3f5934a.png" alt="UTOOLS1589370322613.png" style="zoom:50%;" />

```java
package pers.junebao.simple_factory;

import pers.junebao.simple_factory.fitting.*;
import pers.junebao.simple_factory.phone.Honor;
import pers.junebao.simple_factory.phone.OnePlus;
import pers.junebao.simple_factory.phone.Phone;

public class PhoneFactory {
    /**
     * 一个用来产生 Phone 对象的工厂方法
     * @param name 根据 name 产生不同的 Phone 的子类对象
     * @return 返回实例化后的对象，name 不匹配返回 null
     */
    public static Phone getPhone(String name) {
        if(name.toLowerCase().equals("oneplus")){
            // TODO：使用简单工厂重构
            CPU cpu = new Qualcomm();
            Camera camera = new Sony();
            return new OnePlus(cpu, camera);
        } else if (name.toLowerCase().equals("honor")) {
            CPU cpu = new Kirin();
            Camera camera = new Leica();
            return new Honor(cpu, camera);
        } else {
            return null;
        }
    }
}
```

```java
package pers.junebao.simple_factory;

import pers.junebao.simple_factory.phone.Phone;

public class Consumer {
    public static void main(String[] args) {
        Phone phone = PhoneFactory.getPhone("Honor");
        assert phone != null;
        phone.printConfig();
    }
}

```

[GitHub | 完整代码](https://github.com/520MianXiangDuiXiang520/DesignPatterns/tree/master/src/pers/junebao/simple_factory)

## 策略模式

> 参考：
>
> * [CSDN | 策略模式](https://blog.csdn.net/xingjiarong/article/details/50168853)
> * [百家号 | 策略模式](https://baijiahao.baidu.com/s?id=1638224488060180625&wfr=spider&for=pc)

如果某个系统需要不同的算法（如超市收银的优惠算法），那么可以把这些算法独立出来，使之之间可以相互替换，这种模式叫做策略模式，它同样具有三个角色：

1. 环境角色：使用策略的类
2. 抽象策略角色：策略共有的抽象类或接口
3. 具体策略角色：具体的策略的实现

### 策略模式的优缺点

优点：

1. 需要新的算法时，只需要拓展策略，而不需要修改原有代码，符合开闭原则。
2. 避免出现过多判断分支，提高代码可读性。
3. 算法间可方便的进行继承，替换。

缺点：

1. 客户端必须熟悉所有算法，并自行决定使用哪个策略
2. 策略模式将造成产生很多策略类，可以通过使用享元模式在一定程度上减少对象的数量。

### 适用场景

一个系统中有很多类，这些类之间只有**行为**表现不同时，可以使用策略模式，策略模式在实例化策略时可以配合使用简单工厂。

### 例：

比如一个收银系统，结算时有不同的优惠策略，如 九折， 五折，满100减10等，这些不同的优惠策略便是”具体策略角色“，而收银系统就是 ”环境角色“，还需要定义一个 ”抽象策略角色“：

```java
package pers.junebao.strategy_mode.discount;

// 抽象策略角色
public interface BaseDiscountStrategy {
    double preferentialAlgorithm(double money);
}

```

```java
package pers.junebao.strategy_mode.discount;

// 折扣优惠(具体策略角色)
public class Discount implements BaseDiscountStrategy {
    private double discount;
    public Discount(double discount) {
    // Discount(double discount) {
        if(discount > 1)
            discount = 1;
        else if(discount < 0)
            discount = 0.1;
        this.discount = discount;
    }

    @Override
    public double preferentialAlgorithm(double money) {
        return money * this.discount;
    }
}

```

```java
package pers.junebao.strategy_mode.discount;

// 满减优惠(具体策略角色)
public class FullReduction implements BaseDiscountStrategy {

    private double discountPrice;  //优惠金额
    private double baseline;  // 满减条件

    FullReduction(double baseline, double price) {
        this.baseline = baseline;
        this.discountPrice = price;
    }

    @Override
    public double preferentialAlgorithm(double money) {
        if(money >= this.baseline)
            money -= this.discountPrice;
        return money;
    }
}

```

这样，环境角色就可以自己决定使用哪种策略而不用修改代码了

```java
package pers.junebao.strategy_mode;

import pers.junebao.strategy_mode.discount.BaseDiscountStrategy;
import pers.junebao.strategy_mode.discount.Discount;

public class CashRegisterSystem {
    public static void main(String[] args) {
        BaseDiscountStrategy ds = new Discount(0.9);
        double purchasingPrice = 1500;
        double amountsPayable = ds.preferentialAlgorithm(purchasingPrice);
        System.out.println(amountsPayable);
    }
}
```

对于这些具体策略，可以使用简单工厂，进一步屏蔽策略的具体细节

```java
package pers.junebao.strategy_mode.discount;

public class StrategyFactory {
    public static BaseDiscountStrategy getDiscountStrategy(String name) {
        BaseDiscountStrategy result = null;
        switch (name){
            case "九折":{
                result = new Discount(0.9);
                break;
            }
            case "五折": {
                result = new Discount(0.5);
                break;
            }
            case "满100减10": {
                result = new FullReduction(100, 10);
                break;
            }
            case "满1000减200": {
                result = new FullReduction(1000, 200);
                break;
            }
            default:
                result = new OriginalPrice();
        }
        return result;
    }
}

```



```java
BaseDiscountStrategy ds = StrategyFactory.getDiscountStrategy("满1000减200");
```

[GitHub | 完整代码](https://github.com/520MianXiangDuiXiang520/DesignPatterns/tree/master/src/pers/junebao/strategy_mode)

## 装饰模式

> 装饰模式：动态的给某些对象添加额外的功能
>
> 参考：
>
> * [简书 | 装饰模式](https://www.jianshu.com/p/ff308c759f0a)
>
> * [博客园 | 简说设计模式——装饰模式](https://www.cnblogs.com/adamjwh/p/9036358.html)
>
> *  [博客园 | 装饰器模式 Decorator 结构型 设计模式 (十)](https://www.cnblogs.com/noteless/p/9603041.html)

### 什么是装饰模式

装饰模式也叫装饰器模式，python中的装饰器就是这种模式的体现，对于一个类，如果要添加一个新功能，除了修改代码外（违反开闭原则），可以使用继承，但通过继承添加新功能并不适合所有场景，如

1. 类不可见或不允许继承
2. 需要对一批类似的兄弟类添加同一个新功能时，继承会产生大量的子类
3. 希望新功能的添加和撤销是动态的
4. ......

装饰模式中的对象包括：

1. 装饰器（用来为**被装饰对象**动态添加新功能）

2. 抽象被装饰对象（所有能被装饰对象的抽象）

3. 被装饰对象

客户端如果希望给某个对象动态添加一个新功能，就可以把这个对象（被装饰对象）传递给装饰器，由装饰器实现新功能，并保存一个被装饰对象的引用，并返回给客户端一个装饰器对象，这样，被装饰对象原来的行为和属性并没有改变，甚至被装饰对象本身就没有改变，只是在外面套了一个壳子，新功能是这个壳子提供的。就像TCP/IP协议栈中，应用层的数据包到传输层通过加TCP或UDP首部来传输一样。

### 装饰模式优缺点

优点：

1. 一个装饰器可以给多个不同的类动态添加新功能
2. 新功能由装饰器实现，不需要修改被装饰对象，有一定的安全性
3. 多个装饰器可以配合嵌套使用，以此实现更复杂的功能
4. 新功能不影响原来的功能，添加和撤销都方便

缺点：

1. 过多的装饰类可能使程序变得很复杂

2. > 装饰模式是针对抽象组件（Component）类型编程。但是，如果你要针对具体组件编程时，就应该重新思考你的应用架构，以及装饰者是否合适。当然也可以改变Component接口，增加新的公开的行为，实现“半透明”的装饰者模式。在实际项目中要做出最佳选择。
   >
   > 作者：[慵懒的阳光丶](https://www.jianshu.com/p/ff308c759f0a)

### 适用场景

1. 要添加的新功能与原有类关联不大时
2. 新功能需要方便添加和撤销时
3. 不能或不方便通过继承实现新功能时

### 例

比如卖烤冷面，最基本的就是面（抽象被装饰对象）具体的就是烤冷面（被装饰对象），然后可以往面里面加各种配料（抽象装饰器），如鸡蛋，辣条等（具体装饰器），由于不同配料的加入顺序对最后的烤冷面有影响，所以如果要用继承拓展“烤冷面”，那先加鸡蛋再加辣条和先加辣条再加鸡蛋就需要写两个子类，造成冗余重复，这种场景就适合适用装饰模式。

抽象被装饰对象

```java
package pers.junebao.decorator_pattern;

public abstract class Noodles {
    public String rawMaterial;  // 配料
    public abstract void sayWhoAmI();
}
```

具体的被装饰对象：

```java
package pers.junebao.decorator_pattern;

public class BakedColdNoodles extends Noodles {

    BakedColdNoodles() {
        this.rawMaterial = "面";  // 最原始的烤冷面，配料只有面
    }

    @Override
    public void sayWhoAmI() {
        System.out.println("我是普通烤冷面！");
    }
}

```

抽象装饰器：

```java
package pers.junebao.decorator_pattern.decorator;

import pers.junebao.decorator_pattern.Noodles;

public abstract class Burden extends Noodles {
    public Noodles noodles;  // 装饰器中保留一份被装饰对象的引用，方便客户端使用
    public Burden(Noodles noodles) {
        this.noodles = noodles;
    }
}
```

* 装饰器是为某一类对象提供装饰的（这里就是实现了Noodles 的类）

具体的装饰器类：

* 加鸡蛋

  ```java
  package pers.junebao.decorator_pattern.decorator;
  
  import pers.junebao.decorator_pattern.Noodles;
  
  public class AddEggs extends Burden {
  
      public AddEggs(Noodles noodles) {
          super(noodles);
          this.rawMaterial = noodles.rawMaterial + ", 鸡蛋";
      }
  
  
      @Override
      public void sayWhoAmI() {
          System.out.println("我是加了鸡蛋的烤冷面！！");
      }
  
  }
  ```

* 加辣条

  ```java
  package pers.junebao.decorator_pattern.decorator;
  
  import pers.junebao.decorator_pattern.Noodles;
  
  public class AddSpicyStrips extends Burden{
      public AddSpicyStrips(Noodles noodles) {
          super(noodles);
          this.rawMaterial = noodles.rawMaterial + " ,辣条";
      }
  
      @Override
      public void sayWhoAmI() {
          System.out.println("我是加了辣条的烤冷面！！");
      }
  }
  ```

客户端：

```java
package pers.junebao.decorator_pattern;

import pers.junebao.decorator_pattern.decorator.AddEggs;
import pers.junebao.decorator_pattern.decorator.AddSpicyStrips;

public class Main {
    public static void main(String[] args) {
        Noodles bcn = new BakedColdNoodles();
        Noodles bcnAddEgg = new AddEggs(bcn);
        bcnAddEgg.sayWhoAmI();
        System.out.println(bcnAddEgg.rawMaterial);
        Noodles bcnEggSpicyS = new AddSpicyStrips(bcnAddEgg);
        bcnEggSpicyS.sayWhoAmI();
        System.out.println(bcnEggSpicyS.rawMaterial);
    }
}
/*
我是加了鸡蛋的烤冷面！！
面, 鸡蛋
我是加了辣条的烤冷面！！
面, 鸡蛋 ,辣条
 */
```

这样如果想先加辣条在家鸡蛋，就可以使用AddSpicyStrips先装饰BakedColdNoodles，再用AddEggs装饰AddSpicyStrips。

[GitHub | 完整代码](https://github.com/520MianXiangDuiXiang520/DesignPatterns/tree/master/src/pers/junebao/decorator_pattern)

## 代理模式

> 代理模式( Proxy)：为其他对象提供一种代理以控制对这个对象的访问。
>
> 参考：[refactoringguru | proxy](https://refactoringguru.cn/design-patterns/proxy)

### 什么是代理模式

有时候如果想要访问某个对象，但又没办法直接访问或不方便直接访问，可以使用代理模式，代理模式为想要访问的那个真实对象提供一种“替身”，将客户端直接对服务端的访问转换为客户端只与代理交互，由代理处理具体的和服务端的交互，代理模式有四种角色，分别是：

1. 客户端
2. 服务端
3. 代理
4. 抽象服务接口

<img src="http://yanxuan.nosdn.127.net/6abf9bf54ece17a87a468f3622f5283f.png" alt="UTOOLS1589610468487.png" style="zoom:50%;" />

代理中保留一个真实Server的对象，并且代理和真实Server实现同一个接口，这样对客户端来说Proxy就可以代替Server了，客户端想要调用Server的某个方法时，直接与代理交互，再由代理去调用Server的具体方法。

### 代理的优缺点

优点：

> *  你可以在客户端毫无察觉的情况下控制服务对象。
> *  如果客户端对服务对象的生命周期没有特殊要求， 你可以对生命周期进行管理。
> *  即使服务对象还未准备好或不存在， 代理也可以正常工作。
> *  [开闭原则](https://refactoringguru.cn/didp/principles/solid-principles/ocp)。 你可以在不对服务或客户端做出修改的情况下创建新代理。

缺点：

> *  代码可能会变得复杂， 因为需要新建许多类。
> *  服务响应可能会延迟。

### 代理的类型和使用场景

#### 1. 远程代理

当我们需要一个**远程对象**时，可以通过一个本地代理去访问，所谓远程对象是指远程的资源，包括可能不同命名空间，不同机器的资源等，如果客户端直接访问远程资源，可能涉及到复杂的数据交互和传输，通过代理，我们可以把这些数据交互和传输的过程隐藏在代理里面，由代理去与远程资源交互，并返回客户端需要的数据，这样对客户端来说，访问远程资源就和访问本地资源一样了。以此简化客户端代码。

#### 2. 虚拟代理

虚拟代理的主要作用是**延迟初始化**：

> 如果你有一个偶尔使用的重量级服务对象，一直保持该对象运行会消耗系统资源, 时可使用代理模式.
>
> 你无需在程序启动时就创建该对象， 可将对象的初始化延迟到真正有需要的时候。

比如网站图片的加载, 真实的图片可能很大,如果在构造的时候就直接加载真实的图片,就会导致加载时间过长,所以可以使用代理,用很小的缩略图来代替真实的图片,直到用户点机缩略图时再异步的加载大图.

虚拟代理应该使用缓存避免重量级对象多次重复加载.

#### 3. 保护代理

如果只有拥有特定权限的用户才能访问特定对象,就可以在代理中对用户权限进行判断,并根据权限返回不同的结果.

## 工厂方法模式

> **define an interface or abstract class for creating an object but let the subclasses decide which class to instantiate.**
>
> 参考：
>
> 1. [refactoringguru | factory-method](https://refactoringguru.cn/design-patterns/factory-method)
> 2. [javatpoint | factory-method-design-pattern](https://www.javatpoint.com/factory-method-design-pattern)
> 3. [博客园| 工厂方法](https://www.cnblogs.com/gdwkong/p/8413342.html)

### 简单工厂的问题

简单工厂把可能很复杂的对象创建过程分装在工厂类内部，客户端只需要给简单工厂一个“类的标志”，工厂类就能动态返回一个实例化对象，这样的好处是简化了客户端操作，从客户端按说，符合开闭原则，但每次添加新的产品，都需要修改工厂类，添加新的判断逻辑，不符合**开闭原则**。为了解决简单工厂的这个问题，工厂方法中会先定义一个创建对象的接口或抽象类，然后让子类去决定实例化哪个类。

### 工厂方法的优点

1. 客户端只需要知道产品对应的接口即可，无需关心产品的具体实现细节。
2. 比简单工厂有更好的可拓展性，添加新产品只需要实现接口即可。
3. 耦合度进一步下降。

### 适用场景

1. 如果无法预知对象确切类别及其依赖关系时
2. 需要将类的实例化过程延迟到其子类时
3. 工厂方法可以复用创建好的对象来节省资源（缓存）

### 例

![UTOOLS1589728531095.png](http://yanxuan.nosdn.127.net/f4b1d756e8bcb653606a6a4e3636d3dd.png)

所有工厂类的接口：

```java
public interface IPhoneFactory {
    BasePhone createPhone();
}
```

具体的工厂实现类中实例化产品：

```java
public class HonorFactory implements IPhoneFactory {
    @Override
    public BasePhone createPhone() {
        BaseCPU cpu = new KirinFactory().createCPU();
        BaseCamera camera = new LeicaFactory().createCamera();
        return new Honor(cpu, camera);
    }
}
```

```java
public class OnePlusFactory implements IPhoneFactory {
    @Override
    public BasePhone createPhone() {
        BaseCPU cpu = new QualcommFactory().createCPU();
        BaseCamera camera = new SonyFactory().createCamera();
        return new OnePlus(cpu, camera);
    }
}
```

客户端只需要知道相关接口或抽象类即可，无需关心产品细节

```java
public class Consumer {
    public static void main(String[] args) {
        BasePhone onePlus = new OnePlusFactory().createPhone();
        onePlus.printConfig();
        BasePhone honor = new HonorFactory().createPhone();
        honor.printConfig();
    }
}
```

[GitHub | 完整代码](https://github.com/520MianXiangDuiXiang520/DesignPatterns/tree/master/src/pers/junebao/factory_method)

## 原型模式

> Prototype pattern refers to creating duplicate object while keeping performance in mind. This type of design pattern comes under creational pattern as this pattern provides one of the best ways to create an object.
>
> 参考：
>
> 1. [tutorialspoint | prototype_pattern](https://www.tutorialspoint.com/design_pattern/prototype_pattern.htm)
> 2. [博客园 | 原型模式](https://www.cnblogs.com/fengyumeng/p/10646487.html)
> 3. [博客园 | Java深拷贝与序列化](https://www.cnblogs.com/NaLanZiYi-LinEr/p/9192734.html)

原型模式是通过复制已有对象来快速创建新对象的方法，它适用于创建那些实例化很慢的对象，比如数据库连接对象，在创建好这样的对象后，我们可以缓存一份，下次需要这种对象时，我们可以直接返回一个该对象的拷贝。

### 使用场景

1. 需要大量相似对象时，如果在类中需要大量相似的对象，并且这些对象中有很多属性都是一样的，只有个别属性需要定制时，可以使用原型模式，因为直接从内从中复制对象比new一个新对象的性能要高得多。
2. 如果一个对象的实例化过程很耗时耗力，可以使用原型模式。

### Java Cloneable接口

Java中提供了一个标记接口`Cloneable`，类如果实现了这个接口就可以使用`Object`类中定义的`clone`方法

> 如果没有实现Cloneable接口，直接调用`clone()`会抛出`CloneNotSupportedException`

`Object clone()`会返回当前对象的一个**浅拷贝**

### 深拷贝和浅拷贝

根据不同的对象类型，拷贝的内容也各不相同：

1. **基本数据类型**，如int，char等，直接拷贝**值**
2. 对于**字符串**，拷贝时只复制**引用**，当字符串的值改变时，会从字符串池中重新生成新的字符串，最终结果和拷贝值一样
3. 对于**对象**，拷贝时只**复制引用**，如果要复制值，需要使用**深拷贝**

```java
public class Out implements Cloneable{
    private String outName;
    private In in;

    public Out(String outName) {
        this.outName = outName;
    }

    public void setIn(In in) {
        this.in = in;
    }

    @Override
    public String toString() {
        return "Out{" +
                "outName='" + outName + '\'' +
                ", in=" + in +
                '}';
    }

    @Override
    protected Out clone() throws CloneNotSupportedException {
        return (Out) super.clone();
    }

    public static void main(String[] args) {
        Out out = new Out("out");
        In in = new In("in name");
        out.setIn(in);

        Out out1 = null;
        try {
            // in 是一个object类型，所以在调用clone()时只复制了in的引用
            out1 = out.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
        assert out1 != null;
        // 改变out1.in的name也会改变out中in的name
        out1.in.setName("out1 in");
        System.out.println(out);
        System.out.println(out1);
    }
}
/*
Out{outName='out', in=In{name='out1 in'}}
Out{outName='out', in=In{name='out1 in'}}
*/
```



#### 深拷贝 DeepCopy

Java中实现深拷贝可以手动拷贝object类型的属性，但如果这个类型中还有object类型，就会很麻烦。

```java
@Override
protected DCOut clone() throws CloneNotSupportedException {
    DCOut copy = (DCOut) super.clone();
    In copyIn = (In) this.in.clone();
    copy.setIn(copyIn);
    return copy;
}
```

还可以使用`Serializable`接口，通过序列化，将堆中的对象数据信息复制一份到堆外，再反序列化成新的克隆对象

```java
import java.io.*;

public class DeepClone implements Serializable {
    private Object obj;

    public DeepClone(Object obj){
        this.obj = obj;
    }

    public Object deepClone() {
        Object result = null;
        //序列化
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = null;
        try {
            oos = new ObjectOutputStream(baos);
            oos.writeObject(obj);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // 反序列化
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream  ois = null;
        try {
            ois = new ObjectInputStream(bais);
            result = ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return result;
    }
}

```

#### python中的深拷贝和浅拷贝

```python
In [1]: import copy

In [2]: a = [i for i in range(10)]

In [3]: b = copy.copy(a)

In [4]: a is b
Out[4]: False

In [5]: c = [[1, 2], [3, 4]]

In [6]: d = copy.copy(c)

In [7]: d is c
Out[7]: False

In [8]: d[0] is c[0]
Out[8]: True

In [9]: e = copy.deepcopy(c)

In [10]: e[0] is c[0]
Out[10]: False

In [11]:
```

python内置的copy模块提供了深拷贝和浅拷贝的功能，python中浅拷贝只会拷贝父对象，不会拷贝父对象内部的子对象

> python切片属于浅拷贝

### 例

《大话设计模式》里简历的例子

```java
package pers.junebao.prototype_pattern;

import pers.junebao.prototype_pattern.deep_copy.DeepClone;

import java.io.Serializable;

public class Resume implements Cloneable, Serializable {
    private String name;
    private String education;
    private String sex;

    Resume(String name) {
        this.name = name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setEducation(String education) {
        this.education = education;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }


    public void print(){
        System.out.println("name: " + this.name);
        System.out.println("sex : " + this.sex);
        System.out.println("education: " + this.education);
    }

    @Override
    public Resume clone() {
        Resume resume = null;
        // 深拷贝
        resume = (Resume) DeepClone.deepClone(this);
        return resume;
    }
}

```

```java
package pers.junebao.prototype_pattern;

public class Main {
    public static void main(String[] args) {
        Resume resume = new Resume("JuneBao");
        resume.setSex("男");
        resume.setEducation("本科");
        Resume resume1 = resume.clone();
        resume1.setSex("女");
        resume.print();
        resume1.print();
    }
}
```
[GitHub | 完整代码](https://github.com/520MianXiangDuiXiang520/DesignPatterns/tree/master/src/pers/junebao/prototype_pattern)

## 模板方法

