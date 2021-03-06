# 初始化与清理

## 构造器

类似于C++的构造函数，是一个与类名相同的函数，没有返回值（没有返回值不同于返回NULL），程序执行时会被默认执行。

### 在构造器中使用构造器

* 在构造器中使用构造器，this必须作为第一条语句
* 一个构造器内只能调用一个构造器

```java
package Note;

public class Chapter5_1 {
    // 在构造器中使用构造器
    int num = 0;
    String str = "";

    Chapter5_1(){
//        System.out.println("hello");  // 在构造器中使用构造器，this必须作为第一条语句
        this(5);
//        this(5,"hell0");  // 一个构造器内只能调用一个构造器
        System.out.println("没有参数的构造器");
    }
    Chapter5_1(int n){
        this(n,"hello");
        num = n;
        System.out.println("有一个int参数的构造器");
    }
    Chapter5_1(int n,String s){
        str = s;
        System.out.println("有两个参数的构造器");
    }
    void print(){
        System.out.println("num = " + num + ", str = " + str);
    }

    public static void main(String[] args) {
        Chapter5_1 obj = new Chapter5_1();
        obj.print();
    }
}
//    有两个参数的构造器
//    有一个int参数的构造器
//    没有参数的构造器
//    num = 5, str = hello

```

## 方法重载

### 区分方法重载的两种方法

* 不同的参数类型
* 不同的参数顺序（不推荐使用）
* 不能通过返回值区分重载函数

### 涉及到基本数据类型的方法重载

涉及到基本数据类型的方法重载会到变量提升的问题,如果传入的实参类型小于形参类型，实参数据类型就会被提升，char不同，如果找不到接受char参数的方法，他就会被直接提升为int，如果实参类型大于形参类型（如方法只接受int，传入float）就必须使用类型转换窄化实参，否则会报错。

```java
public class Chapter5_1 {
    // 涉及到基本数据类型的方法重载
    void demo(int i){
        System.out.println("a int args");
    }

    public static void main(String[] args) {
        Chapter5_1 c = new Chapter5_1();
        c.demo('x');
    }
}
```

## this

类似于python中的self和JavaScript的this。  
在方法内部调用同一类的别的方法是可以不使用this

## 垃圾回收和终结处理

## 初始化

### 成员初始化

允许在定义类属性时直接为其赋初值（C++ 不允许）

### 构造器初始化

可以使用构造器初始化类属性。

#### 初始化顺序

在类的内部，变量定义的顺序取决于初始化的顺序，即使变量定义散布于方法定义之间，他们人会在方法之前得到初始化（包括构造器），也就是变量定义会比方法优先执行，以确保变量有初值，这与JavaScript很像。

```java
package Note;

/**
 * 在类的内部，变量定义的先后顺序取决于初始化的顺序，即使变量定义散布于方法定义间，他们仍会在任何方法之前得到初始化
 */

class Window {
    Window(int no){
        System.out.println("Chapter5_7:" + no + ";");
    }
}
class House{
    House(){
        System.out.println("Chapter5_7构造器");
        Window d1 = new Window(1);
    }
    Window d2 = new Window(2);
    void c1(){
        System.out.println("c1()");
    }
    Window d3 = new Window(3);
}
public class Chapter5_7 {
    public static void main(String[] args) {
        House house = new House();
        house.c1();
    }
}
//Chapter5_7:2;
//Chapter5_7:3;
//Chapter5_7构造器
//Chapter5_7:1;
//c1()

```

#### 静态数据初始化

无论创建多少个对象，静态数据始终只占一块存储空间，所以即使重复定义初始化它也不会重复初始化

```java
package Note;

class Bowl{
    Bowl(int marker){
        System.out.println("Bowl (" + marker + ")");
    }
    void f1(int marker){
        System.out.println("f1(" + marker + ")");
    }
}

class Table{
    static Bowl bowl1 = new Bowl(1);
    Table(){
        System.out.println("Table()");
        bowl2.f1(1);
    }
    void f2(int marker){
        System.out.println("f2(" + marker + ")");
    }
    static Bowl bowl2 = new Bowl(1);
}

class Cupboard{
    Bowl bowl3 = new Bowl(3);
    static Bowl bowl4 = new Bowl(4);
    Cupboard(){
        System.out.println("Cupuoard()");
        bowl4.f1(2);
    }
    void f3(int marker){
        System.out.println("f3(" + marker + ")");
    }
    static Bowl bowl5 = new Bowl(5);
}

public class Chapter5_7_2 {
    public static void main(String[] args) {
        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        table.f2(1);
        cupboard.f3(1);
    }
    static Table table = new Table();
    static Cupboard cupboard = new Cupboard();
}

//Bowl (1)
//Bowl (1)
//Table()
//f1(1)
//Bowl (4)
//Bowl (5)
//Bowl (3)
//Cupuoard()
//f1(2)
//Creating new Cupboard() in main
//Bowl (3)
//Cupuoard()
//f1(2)
//Creating new Cupboard() in main
//Bowl (3)
//Cupuoard()
//f1(2)
//f2(1)
//f3(1)

```

程序从Chapter5_7_2类开始，由于静态变量table和cupboard都没有被创建过，所以先执行变量定义，进入Table类，brow1，brow2都未被创建，也会优先执行变量创建，再进入Brow类，执行Brow的构造器，然后执行Table的构造器，table变量创建完毕，cupboard一样，bowl3是普通变量，bolw4和5是静态变量，45先创建，再创建3，最后执行main，执行到`new Cupboard();`时，依旧是先创建静态变量，在创建普通变量，最后执行方法，不过两个静态变量已经在创建cupboard时创建，不会被重复创建，只创建bowl3

#### 显式的静态初始化

允许多个静态化语句组成一个静态块

```java
package Note;

class Cup {
    Cup(int marker){
        System.out.println("Cup:(" + marker + ")");
    }
    void f(int marker){
        System.out.println("f (" + marker + ")");
    }
}

class Cups{
    static Cup cup1;
    static Cup cup2;
    // 静态块
    static{
        cup1 = new Cup(1);
        cup2 = new Cup(2);
    }
    Cups(){
        System.out.println("cups()");
    }
}

public class Chapter5_7_3 {
    public static void main(String[] args) {
        System.out.println("main()");
        Cups.cup1.f(99);  // 使用类名调用静态属性
    }
}

//main()
//Cup:(1)
//Cup:(2)
//f (99)
```

```java
public class Chapter5_7_3 {
    public static void main(String[] args) {
        System.out.println("main()");
        cups1.cup1.f(99);
    }
    static Cups cups1 = new Cups();
}
// Cup:(1)
// Cup:(2)
// cups()
// main()
// f (99)
```

#### 非静态实例初始化

```java
package Note;

class Mug {
    Mug(int marker){
        System.out.println("Mug(" + marker + ")");
    }
    void f(int marker){
        System.out.println("f(" + marker + ")");
    }
}

public class Chapter5_7_4 {
    // 实例初始化，只要调用显式构造器，实例初始化语句就会被执行
    Mug mug1;
    Mug mug2;
    {
        mug1 = new Mug(1);
        mug2 = new Mug(2);
        System.out.println("mug1 & mug2 initialized");
    }
    Chapter5_7_4(){
        System.out.println("Chapter5_7_4()");
    }
    Chapter5_7_4(int i){
        System.out.println("Chapter5_7_4(int)");
    }

    public static void main(String[] args) {
        System.out.println("main()");
        new Chapter5_7_4();
        System.out.println("create Chapter5_7_4()");
        new Chapter5_7_4(1);
        System.out.println("create Chapter5_7_4(int)");
    }
}

//main()
//Mug(1)
//Mug(2)
//mug1 & mug2 initialized
//Chapter5_7_4()
//create Chapter5_7_4()
//Mug(1)
//Mug(2)
//mug1 & mug2 initialized
//Chapter5_7_4(int)
//create Chapter5_7_4(int)

```

### 数组初始化

编译器不允许定义数组的大小，使用`int [] array`创建的只是一个数组的引用，并没有给数组对象本身分配任何内存空间，为了给数组创建相应的存储空间，必须使用初始化表达式，对于数组，初始化动作可以发生在代码的任何地方，但`int [] array = {1, 2, 3}`这种形式的初始化必须出现在数组创建的地方。  

如果不确定数组大小，可以使用new动态创建数组`int [] array = new int [10]`,这个10可以是一个变量，对于基本数据类型，这样创建数组后，数组中的元素会有初值，但对于其他数据类型不行。

```java
public class Chapter5_8 {
    public static void main(String[] args) {
        // 基本数据类型
        int [] array_int = new int [20];
        for(int i: array_int){
            System.out.print(i);
        }
        System.out.println();
        // 非基本数据类型
        Integer [] array_integer = new Integer[20];
        for(int i=0;i<array_integer.length;i++){
            array_integer[i] = new Integer(0);
        }
        for(int i: array_integer){
            System.out.print(i);
        }
    }
}

```

对于非基本数据类型的数组，使用new（`Integer [] array_integer = new Integer[20];`）也只是创建了一个引用数组，只有只有创建了新的Integer对象，并把这个对象赋值给引用，才算初始化了数组。  
还有两种方法可以创建数组：

```java
Integer [] a;
        a = new Integer[]{
                new Integer(1),
                new Integer(2),
        };

        for(Integer i: a){
            System.out.print(i);
        }

        System.out.println();
        Integer [] b = {
                new Integer(1),
                new Integer(2),
        };
        for(Integer i: b){
            System.out.print(i);
        }
```

#### 可变参数列表

## 枚举类型enum

创建枚举类型

```java

public class Chapter5_9 {
    public enum Spiciness{
        NOT, MILD, MEDIUM, HOT, FLAMING
    }
}
```

使用枚举类型

```java
public static void main(String[] args) {
        // 为了使用enum，需要创建一个该类型的引用
        Spiciness howhot = Spiciness.MEDIUM;
        System.out.println(howhot);
        for(Spiciness s: Spiciness.values()){
            System.out.println(s + "(" + s.ordinal() + ")");
        }
    }
```

创建枚举类型时，编译器会自动添加一些有用的方法：

* toString()
* ordinal():表示特定enum常量的声明顺序
* static values():根据声明顺序将常量值构成数组

enum与switch

```java
public class Chapter5_9 {
    public enum Spiciness{
        NOT, MILD, MEDIUM, HOT, FLAMING
    }
    Spiciness degree;

    Chapter5_9(Spiciness degree){
        this.degree = degree;
    }

    public void describe(){
        System.out.print("This burrito is ");
        switch(this.degree){
            case NOT:
                System.out.println("not spicy at all");
                break;
            case MILD:
            case MEDIUM:
                System.out.println("a little hot");
                break;
            case FLAMING:
            case HOT:
                default:
                System.out.println("maybe too hot.");
        }
    }

    public static void main(String[] args) {
        Chapter5_9
                plain = new Chapter5_9(Spiciness.NOT),
                greenChile = new Chapter5_9(Spiciness.MEDIUM),
                jalapeno = new Chapter5_9(Spiciness.HOT);
                plain.describe();
                greenChile.describe();
                jalapeno.describe();
    }
}

```

## 总结

* 函数重载
  * 区分方法重载：不同的参数类型，不同的参数顺序（不推荐），不能使用返回值区分方法
  * 实参类型应该小于或等于形参类型，实参小于形参会被提升
  * 对于char型（单引号）实参，找不到对应的参数会被转换为int
* 构造器
  * 无返回值，可重载，与类同名
  * 在构造器中使用构造器：this作为第一条语句，只出现一次
  * static的含义，没有this
* 初始化：
  * 构造器初始化
    * 执行代码前，变量优先初始化
    * 静态数据只初始化一次，可以使用静态块初始化
    * 非静态实例初始化：只要显式调用了构造器，实例初始化块中的代码就会被执行
  * 成员初始化（允许直接赋初值）
  * 数组初始化
    * 定义一个数组只是定义了一个引用，必须使用相应的初始化语句
    * 对于基本数据类型，用new可以为数组分配内存，并赋初值
    * 对于非基本数据类型，使用new之后也还是一个引用，只有创建了一个新的对象并赋值给这个引用才行
* 枚举类型
  * enum
  * values()
  * ordinal()
