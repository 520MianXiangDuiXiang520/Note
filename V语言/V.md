# V语言极限学习

我听说V语言看文档半小时就能完全掌握？？？？以我的智商一小时掌握不了我就给各位科普一下广告法？？？

## 宇宙惯例hello world

```v
// first v code
fn main(){
    printIn("hello world")
}
```

* 不需要行结束符
* v函数使用`fn`声明，和其他语言一样，main函数是程序入口
* 注释规则和c一样
* 输出使用内置函数 `printIn()`

## 宇宙惯例2. 1+1

```v
fn main(){
    a := 1
    b := 2
    mut name := "v langue"
    name = "v"
    printIn(add(a,b))
}
fn add(a int,b int) int {
    return a+b
}
```

* 变量名在类型名之前（反人类）
* 函数和变量都可以提前，也就是可以“先调用，再声明”
* 变量用`:=`声明并初始化，变量默认不允许修改，要修改必须加 `mut`
* 修改变量用 `=`
* v没有全局变量，变量只能在函数中定义
* 定义的变量必须使用，不允许只定义，不使用，和go像
* 子代码块中不允许使用父代码块中已经定义的变量,如下面的代码会编译出错

```v
fn main(){
    a := 20
    if true{
        a := 30
    }
}
```

## 基本数据类型

### string

在V中，字符串是只读字节数组。 字符串数据使用UTF-8编码。

单引号和双引号都可用于表示字符串（TODO：尚不支持双引号）。 为保持一致性，vfmt将双引号转换为单引号，除非该字符串包含单引号字符。

字符串是不可变的。 这意味着子字符串函数非常有效：不执行复制，不需要额外的分配。

>All operators in V must have values of the same type on both sides. This code will not compile if age is an int:
>println('age = ' + age)
>We have to either convert age to a string:
>println('age = ' + age.str())
>or use string interpolation (preferred):
>println('age = $age')
>
>翻译
>V中的所有运算符必须在两边都具有相同类型的值。如果age是int: println('age = ' + age')，这段代码将无法编译。我们必须将age转换为一个字符串:println('age = ' + age.str())或使用字符串插值(preferred): println('age = ' $age')

### 数组

```v
fn main(){
    a := [1,2,3]
    printIn(a)
}
```

* 数组类型由数组第一个元素决定
* 数组中元素类型必须相同
* 使用`<<`在数组末尾插入元素
* 使用`.len`返回数组长度
* `val in array`,如果数组array包含val，返回true

### 字典

```v
mut m := map[string]int{} // Only maps with string keys are allowed for now  
m['one'] = 1
println(m['one']) // ==> "1" 
```

这个字典人家似乎还没有写好，emmmm，一堆TODO，你先写着，咱不急，看下一个

## 流程控制

### if

```v
a := 10 
b := 20 
if a < b { 
	println('$a < $b') 
} else if a > b { 
	println('$a > $b') 
} else { 
	println('$a == $b') 
} 
```

* 条件没有小括号
* 始终有大括号
* if语句可以作为一个表达式

```v
num := 777
s := if num % 2 == 0 {
	'even'
}
else {
	'odd'
}
println(s) // ==> "odd"
```

### in

作用：

1. 检查数组中是否含有某个元素
2. 布尔表达式，如：

```v
if parser.token == .plus || parser.token == .minus || parser.token == .div || parser.token == .mult {
	... 
} 

if parser.token in [.plus, .minus, .div, .mult] {
	... 
} 
```

上下两个是等价的，使用下面的语法时，v不会创建数组

### for

for比较牛逼，因为我看他文档写的比之前的都多....(狗头)，知道为啥吗，应为v只有一种循环，就是for，哈哈哈哈

虽然只有一种循环，但人家for有好几种啊~~~

#### for in

```v
fn main(){
    list := ['a','b','c']
    for value in list{
        printIn(value)
    }
}

```

value-in

如果需要数据的索引，可以用另一种方法

```v
names := ['Sam', 'Peter']
for i, name in names {
    println('$i) $name')  // Output: 0) Sam
}                         //         1) Peter

```

#### 第二种for(类似于while)

```v
mut sum := 0
mut i := 0
for i <= 100 {
	sum += i
	i++
}
println(sum) // ==> "5050"
```

* 不写条件将导致死循环

#### 第三种for(类似c)

```v
for i := 0; i < 10; i++ {
	println(i)
}
```

* 为啥这儿的i不用加mut而可以变化？？别问，文档这么写的！！！

>Here i doesn't need to be declared with mut since it's always going to be mutable by definition.

### switch

```v
os := 'windows' 
print('V is running on ')
switch os {
case 'darwin':
	println('macOS.')
case 'linux':
	println('Linux.')
default:
	println(os) 
}
```

这里的switch和c里的差不多，只不过v中不需要在每个case后面加break

## 结构体

结构体？？？你可别告诉我你面向过程啊

```v
struct Point {
	x int
	y int 
} 

p := Point{
	x: 10 
	y: 20 
} 
println(p.x) // Struct fields are accessed using a dot 

```

* 属性访问用.
* 结构是在堆栈上分配的。若要在堆上分配结构并获取指向它的指针，请使用&,如

```v
pointer := &Point{10, 10}  // 有三个或更少字段的结构体可使用这种替代写法
println(pointer.x) // 用指针访问值和其他一样，都用.  
```

* 结构体嵌套，目前还不支持，不过快了

```v
// 就直接复制了，他支持了再说（到时候我也不一定看）
V doesn't have subclassing, but it supports embedded structs:

// TODO: this will be implemented later in June
struct Button {
	Widget
	title string
}

button := new_button('Click me')
button.set_pos(x, y)

// Without embedding we'd have to do
button.widget.set_pos(x,y)
```

## 访问修饰符

默认的结构体是私有的，不可变的，可以使用访问修饰符pub 和 mut 修改，pub和mut有五种组合（不明白了吧，还有一种pub mut mut）,先把文档复制过来再看是个什么妖魔

```v
struct Foo {
	a int     // private immutable (default) 
mut: 
	b int     // private mutable 
	c int     // (you can list multiple fields with the same access modifier)   
pub: 
	d int     // public immmutable (readonly) 
pub mut: 
	e int     // public, but mutable only in parent module  
pub mut mut: 
	f int 	  // public and mutable both inside and outside parent module  
}                 // (not recommended to use, that's why it's so verbose) 
```

|访问修饰符|作用|
|---------|----|
|不写（默认）|私有，不可变|
|mut|私有，可变|
|pub|公有，不可变|
|pub mut|公有，仅在父模块可变|
|pub mut mut|公有，父模块内部外部都可变|

一脸懵逼是吧，哈哈哈，依老衲看来，这和c++中的public，private啥的一样，只不过他的变量（不能叫变量吧，先这样叫）默认是常量（const）你定义时需要加一个mut才能变成其他语言的“变量”，加一个pub这个变量就变成公有变量，从结构体外部可以访问了，加一个pub mut他就在结构体内外可以访问，而只能在结构体内部能改变，如字符串结构体中的len，外部可以访问他，但不能改变它，内部才能改变，最后pub mut mut 就是内外都可以访问，都可以修改。

## Methods，方法

v没有class 吓死我了，辛亏有方法

一个方法就是一个函数，它带一个特殊的参数（接收器）

```v
// 继续粘贴文档代码，CV工程师，年薪百万，啊啊啊啊啊啊啊啊
struct User {
	age int 
} 

fn (u User) can_register() bool {
	return u.age > 16 
} 

user := User{age: 10} 
println(user.can_register()) // ==> "false"  

user2 := User{age: 20} 
println(user2.can_register()) // ==> "true"
```

* 这里的can_register就是一个方法，他的接收器是u，类型是User，官方说接收器名字最好用简短的，别用self，this啥的，一个字母最好（要不然没特色，开玩笑的）

## Pure functions by default

英语捉急，无法翻译，大概就是默认的纯函数，应为V没有全局变量，加上变量默认不能改变，哪怕是传参时也一样，

**后面开始赋值粘贴了**

```
struct User {
mut:
	is_registered bool 
} 

fn (u mut User) register() {
	u.is_registered = true 
} 

mut user := User{} 
println(user.is_registered) // ==> "false"  
user.register() 
println(user.is_registered) // ==> "true"  
```

```v
fn multiply_by_2(arr mut []int) {
	for i := 0; i < arr.len; i++ {
		arr[i] *= 2
	}
}

mut nums := [1, 2, 3]
multiply_by_2(mut nums)
println(nums) // ==> "[2, 4, 6]"

```

* 注意，在调用此函数时，必须在nums之前添加mut。 这清楚地表明被调用的函数将修改该值。
* 最好返回值而不是修改参数。修改参数应该只在应用程序的性能关键部分执行，以减少分配和复制。
* 使用user.register()或user = register(user)代替register(mut user)。
* V可以很容易地返回对象的修改版本：

```v
fn register(u User) User { 
	return { u | is_registered: true } 
}

user = register(user) 
```

## 常量const

```v
const (
	PI    = 3.14
	World = '世界'
) 

println(PI)
println(World)
```

* 常量使用const声明。
* 它们只能在模块级别(函数之外)定义。
* 常量名称必须大写。这有助于将它们与变量区分开来。
* 常数永远不会改变。
* V常量比大多数语言更灵活。您可以分配更复杂的值

```v
struct Color {
        r int
        g int
        b int
}

fn (c Color) str() string { return '{$c.r, $c.g, $c.b}' }

fn rgb(r, g, b int) Color { return Color{r: r, g: g, b: b} }

const (
        Numbers = [1, 2, 3]

        Red  = Color{r: 255, g: 0, b: 0}
        Blue = rgb(0, 0, 255)
)

println(Numbers)
println(Red)
println(Blue)
```

* 不允许使用全局变量，因此这非常有用。

## 模块化

V是一种非常模块化的语言。鼓励创建可重用模块，而且非常简单。要创建一个新模块，请创建一个目录，其中包含模块的名称和.v文件

```v
cd ~/code/modules
mkdir mymodule
vim mymodule/mymodule.v

// mymodule.v
module mymodule

// To export a function we have to use `pub`
pub fn say_hi() {
	println('hello from mymodule!')
}
```

你可以在mymodule /中拥有尽可能多的.v文件。
使用v -lib~ / code / modules / mymodule构建它。
就是这样，您现在可以在代码中使用它

```v
module main

import mymodule

fn main() {
	mymodule.say_hi()
}
```

* 注意，每次调用外部函数时都必须指定模块。
* 模块名称应该简短，不超过10个字符。
* 不允许循环导入。
* 您可以在任何地方创建模块。
* 所有模块都被静态地编译成一个可执行文件。