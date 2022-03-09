# Python3.10 结构化模式匹配 PEP 634

眼看 2021 马上结束，python 发布了它的 3.10 版本，优化了错误消息，上下文管理器等内容，但更吸引我的还是结构化模式匹配。

<!-- more -->

众所周之 `switch` 一直是 python 社区呼声比较高的一个功能，这次发布的结构化模式匹配 `match` 在功能上应该比 Java 或 C 中的这种 `switch` 强大一点。

`match` 的语法类似于其他语言的 `switch`:

```python
def demo(code: int) -> str:
    match code:
        case 200 | 201 | 202:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "Internal Error"

if __name__ == "__main__":
    print(demo(200))
```

值得注意的是 `match` 语句中没有 `default` 关键字，而是使用一个 `_` 代替。`match` 会 **从上到下** 匹配 case 直到匹配成功或遇到 `_` 跳出 `match` 结构. 多个相同行为的匹配项可以使用 `|` 连接

注意 `_` 只能放在最后一个 case 的位置，否则会抛出异常：

```python
case _:
     ^
SyntaxError: wildcard makes remaining patterns unreachable
```

除了匹配常量， `match` 还可以匹配变量，看官网这个例子：

```python
def demo3(pos):
    match pos:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")

if __name__ == "__main__":
    demo3((0, 1))  # Y=1
```

行为类似于将一个元组解包为 x 和 y 再匹配, 在这种模式下， `_` 有了新的用途，它可以表示一个通配符，如：

```python
def demo6(log):
    match log:
        case ('warning', code, 40):
            print("A warning has been received.")
        case ('error', code, _):
            print(f"An error {code} occurred.")

if __name__ == "__main__":
    demo6(("error", 400, 80)) # An error 400 occurred.
```

除此之外， `match` 还可以根据类的属性进行匹配，如下：

```python
class Player:
    def __init__(self, role: int, online: bool):
        self.role = role
        self.online = online

def demo4(p: Player):
    match p:
        case Player(role=1, online=False):
            print("role 1 offline")
        case Player(role=1, online=True):
            print("role 1 online")
        case _:
            print("not role 1")

if __name__ == "__main__":
    demo4(Player(1, True))
```

你甚至可以嵌套使用上面这些特性：

```python
def demo5(role: int, online: bool):
    match [Player(role, online)]:
        case []:
            print("empty player box")
        case [Player(role=role, online=False)]:
            print(f"role {role} offline")
        case [Player(role=role, online=True)]:
            print(f"role {role} online")
        case _:
            print("bad player box")

if __name__ == "__main__":
    demo5(2, False)
```

如果你的匹配条件很复杂，你甚至可以像下面这样在 case 语句上加守护项：

```python
def demo7(log):
    match log:
        case ('warning', code, 40):
            print("A warning has been received.")
        case ('error', code, _) if code in range(400, 500):
            print(f"An client error {code} occurred.")
        case ('error', code, _) if code in range(500, 600):
            print(f"An server error {code} occurred.")
if __name__ == "__main__":
    demo7(("error", 418, 80)) # An client error 418 occurred.
    demo7(("error", 512, 80)) # An server error 512 occurred.
```

总之，`match` 确实能减少某些场合下的开发负担，但很害怕未来 Python 为了功能 “全” 而变得越来越复杂和臃肿。

还有一些其他发布的新功能和特性参见 [whatnew 3.10](https://docs.python.org/zh-cn/3/whatsnew/3.10.html#pep-634-structural-pattern-matching)