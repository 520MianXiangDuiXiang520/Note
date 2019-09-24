# Java访问权限控制

## 包

* 使用package控制包中的类
* import的查找路径是环境变量CLASSPATH+import后面的路径
* 使用import static导入静态属性或方法

## Java访问权限

有四种，public，protected，private，包访问权限

* 包访问权限
  * 没有申明访问权限就是包访问权限(friendly)
  * 拥有包访问权限可以在同一个包内自由访问，而对别的包则表现为私有
* public 接口访问权限
  * 全局都可以访问
  * 作为外部接口
* private 私有成员
  * 仅在本类内可用
* protected 继承访问权限
  * 子类可用
  * 具有包访问权限

## 类的访问权限

类的权限只能是包访问权限或public，不能是private或protected，不希望其他人获得改类的任何实例，需要把所有构造器声明为private，这时候只能通过该类内部的static成员实例化该类。

```java
// Note/chapter6_4/Soup.java
package Note.chapter6_4;
import static junbao.tool.Print.*;

class Soup {
    private static int nums = 0;
    private Soup(){
        this.nums ++;
        coutln("beautiful soup :  " + this.nums);
    }
    public static Soup makeSoup(){
        return new Soup();
    }
}

class Soup2{
    private int nums = 0;
    private Soup2(){
        this.nums ++;
        coutln("beautiful soup2 : " + this.nums);
    }
    // 单例模式
    private static Soup2 soup2 = new Soup2();
    public static Soup2 makeSoup2(){
        return soup2;
    }
}
```

```java
// Note/chapter6_4/Lunch.java
package Note.chapter6_4;
import static Note.chapter6_4.Soup.*;
import static Note.chapter6_4.Soup2.*;

public class Lunch {
    public static void main(String[] args) {
        // Soup中所有构造器都被声明为private，类外无法创建实例
        // Soup s = new Soup();
        Soup soup = makeSoup();
        makeSoup();
        makeSoup();
        Soup2 Soup2 = makeSoup2();
        makeSoup2();
        makeSoup2();
    }
}
// beautiful soup :  1
// beautiful soup :  2
// beautiful soup :  3
// beautiful soup2 : 1

```
