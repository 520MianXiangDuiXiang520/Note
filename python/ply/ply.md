# Ply

Ply 是一个纯 python 的词法分析和语法分析库，包括两个模块：lex 和 yacc

* lex 用于将输入的文本通过正则表达式转换为一系列 Token
* yacc 用作上下文无关语法分析

## lex 词法分析

使用 lex 词法分析最重要的是定义 token 及其解析规则，每个词法分析程序都必须定义 `tokens` 元组用于声明 TOKEN：

```python
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)
```

TOKEN 的解析规则通过 `t_token_name` 来定义，支持这样三种方式：

1. 对于非常简单的规则，你可以简单地定义上面格式的字符串去声明，如： `t_PLUS = r'\+'`
2. 对于复杂的规则，你可以定义如下格式签名的函数去声明：
   
    ```python
    def t_NUMBER(t: lex.LexToken):
        r'\d+'
        t.value = int(t.value)    
        return t
    ```

    正则表达式在函数的文档字符串中指定, 参数固定是 `lex.LexToken` 的实例，它包含四个基本属性：

    * `type`: 类型，就是 tokens 中定义的某个字符串
    * `value`: 对应的值
    * `lineno`: 第几行
    * `lexpos`: 文本起始位置偏移值
3. 如果你的表达式更加复杂，由多个子表达式组合而成，文档字符串无法满足时就可以使用 `@TOKEN` 注解，如：
   ```python
    digit            = r'([0-9])'
    nondigit         = r'([_A-Za-z])'
    identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'   

    @TOKEN(identifier)
    def t_ID(t):
        # want docstring to be identifier above. ?????
        return t
   ```

需要注意的是 tokens 列表中的 TOKEN 是有顺序的，靠前的 TOKEN 将优先被解析，如在定义 `=` 和 `==` 的时候，你可能就需要将后者放在前面。

### 特殊规则

1. 跳过注释:

    ```py
    def t_COMMENT(t):
        r'\#.*'
        pass
        # No return value. Token discarded
    ```

    或者，您可以在token声明中包含前缀“ignore_”，以强制忽略token。例如: ` t_ignore_COMMENT = r'\#.*'
`
2. 定义行：您可以使用 `t_newline(t)` 告诉词法分析器什么是一个新行，这样分析器就可以正确地更新 `lineno` 了，如：
   ```py
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
   ```
3. 定义错误信息，当词法分析出现错误时，你应该明确的告诉用户哪儿错了，使用 `t_error` 来声明错误提示信息，如下：
   ```py
    def t_error(t):
        print(f"Illegal character '{t.value}' in {t.lineno}:{t.lexpos}")
        t.lexer.skip(1)
   ```
4. EOF 处理：有时你需要告诉解析器什么时候该结束，又或者你不想一次性将要解析的源文件加载到内存中，想逐批加载分析，这时候可以使用 `t_eof(t)` 告诉解析器结束时该干什么：
   ```py
    def t_eof(t):
        # Get more input (Example)
        more = raw_input('... ')
        if more:
            self.lexer.input(more)
            return self.lexer.token()
        return None
   ```

### 一些小技巧

1. 单个字符可以使用 `literals` 更方便地指定，如：
    ```py
    literals = [ '+','-','*','/' ]
    # 或
    literals = "+-*/"
    ```
    但需要注意的是这样指定得到的 value 和 type 都是字符本身，你可以像下面这样编写代码修改这个行为：
    ```py
    def t_add(t: lex.LexToken):
        r'\+'
        t.type = "ADD"
        return t
    ```
2. 有时你可能想定义一些关键字，如 `if else` 之类的，为每个关键字定义解析规则可能有点麻烦，这时候将他们作为单词的一部分去解析可能更高效：
   ```py
    tokens = ("CHAR")

    reserved2 = {
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
        'while' : 'WHILE',
    }

    tokens += tuple(reserved2.values())


    def t_CHAR(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved2.get(t.value,'ID')
        return t
   ```
3. 跳过空格之类无意义的填充符号有时也是非常必要的，你可以使用 `t_ignore` 标注这些字符，可以放心的是当这些字符被包含在其他规则中时，它将不会被忽略，使用如下：
   ```py
    t_ignore = (" ")
   ```

### 工程化

通过上面的介绍，你可能已经发现，ply 包含太多特殊规则了，对于一个不了解 ply 的人来说，这可能太糟糕了，我们需要一些办法来稍稍改善它。

1. 你可以在单独的模块中定义规则，以此保证分析器主代码干净，这需要你在创建 lexer 时显式地指定 module：
   ```py
    lexer = lex.lex(module=tokrules)
   ```
2. 面向对象：有时面向对象不失是一个封装的好办法，你可以以面向对象的方式编写规则，如下：
   ```py
    import ply.lex as lex


    class MyLexer:
        reserved = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'while': 'WHILE',
        }
        tokens = ("NUMBER", "CHAR") + tuple(reserved.values())
        literals = ['+', '-', '*', '/']
        t_ignore = (" ")

        def __init__(self, **kwargs) -> None:
            self.lexer: lex.Lexer = lex.lex(module=self, **kwargs)

        def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
            r'\d+'
            t.value = int(t.value)
            return t

        def t_CHAR(self, t: lex.LexToken) -> lex.LexToken:
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = self.reserved.get(t.value, 'CHAR')
            return t

        def t_error(self, t: lex.LexToken) -> lex.LexToken:
            print(f"Illegal character '{t.value}' in {t.lineno}:{t.lexpos}")
            t.lexer.skip(1)

        def run(self, data):
            self.lexer.input(data)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                print(tok)


    if __name__ == "__main__":
        data = "if +12 +3"
        lexer = MyLexer()
        lexer.run(data)
   ```
3. 当然，你也可以用闭包去做，但我个人是一个彻底的闭包反对者，所以不多做介绍……

### 状态跳转

考虑你正在写一个 MarkDown 的分析器，你可能需要做这样的事情：

* 如果遇到 "\`\`\`python" 就开始按 python 的语法规则解析后面的内容知道遇到 "\`\`\`"
* 如果遇到 "\`\`\`c" 就开始按 C 的语法规则解析后面的内容知道遇到 "\`\`\`"
* 其余时候按 MarkDown 的规则解析

要处理这样的需求最好是给分析器提供不同的状态和指定在某种状态下的解析规则，在 ply 中，你可以使用 `states` 定义一组状态：

```py
states = (
    ('py','exclusive'),
    ('c','inclusive'),
 )
```

每种状态有两种类别，分别是 exclusive 和 inclusive：exclusive 表示独占，编译器跳转到这种状态时将会完全使用该状态的词法规则覆盖原来的规则，例如上面的例子就适合 exclusive 类型；inclusive：exclusive 表示包含，跳转到这种状态时，编译器将会将该状态的规则追加到原来的规则列表中。

一旦定义了 states 你就需要在定义每个规则时显式声明它属于那种状态，方法如下：

```py
t_py_NUMBER = r"\d+"

def t_c_error(t: lex.LexToken):
    pass
```

如果你的规则适用于任何状态，可以使用 `ANY` 签名：

```py
def t_ANY_newline(t):
     r'\n'
     t.lexer.lineno += 1
```

当然，显式地指定每个状态也是可以的，像这样：

```py
def t_py_c_newline(t):
     r'\n'
     t.lexer.lineno += 1
```

lexing 的默认状态叫 `INITIAL`, 你可以在规则中通过 `begin` 函数切换状态，如：

```py
def t_md_CHAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == "```py":
        t.lexer.begin("py")
    elif t.value == "```":
        t.lexer.begin("INITIAL")
    return t
```

使用 `push_state()` 和 `pop_state()` 也可以完成相同的操作，如：

```py
def t_md_CHAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == "```py":
        t.lexer.push_state("py")
    elif t.value == "```":
        t.lexer.pop_state()
    return t
```

## 语法分析

ply 使用 LR 解析，关键模块是 `ply.yacc`, 类似于词法分析，你需要按照一定的格式定义你的语法分析规则，假设给定以下语法规范：

```c
 expression : expression + term
            | expression - term
            | term
 
 term       : term * factor
            | term / factor
            | factor
 
 factor     : NUMBER
            | ( expression )
```

它是一个简单地算数表达式的语法规则，在 ply 中，我们可以这样去描述它：

```py
def p_expression_plus(p):
    '''expression : expression '+' term'''
    p[0] = p[1] + [3]

def p_expression_minux(p):
    '''expression : expression '-' term'''
    p[0] = p[1] - [3]

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_times(p):
    '''term : term "*" factor'''
    p[0] = p[1] * [3]

def p_term_div(p):
    '''term : term "/" factor'''
    p[0] = p[1] / [3]

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUMBER'''
    p[0] = p[1]

def p_factor_expr(p):
    '''factor : "(" expression ")"'''
    p[0] = p[2]
```

作为一种更简洁的写法，你可以将多个语法规则写到一个描述函数中，就像下面这样：

```py
def p_expression(p):
    '''expression : expression "+" term
                  | expression "-" term
                  | term'''
    match p[2]:
        case "+" if len(p) > 3:
            p[0] = p[1] + p[3]
        case "-" if len(p) > 3:
            p[0] = p[1] - p[3]
        case _ if len(p) == 2:
            p[0] = p[1]
```

你当然可以可以将所有规则放在一个函数中，但出于可读性和性能，请不要那样做。

你可能注意到了上面示例中的单个字符如 `+-*/` 都被引号印了起来，这是有必要的，这种做法对应词法分析中讲过的 `literals` 如果你不喜欢使用它，可以使用更普遍的做法：

```py
def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = p[1] + [3]
```

你可以使用特殊的 `p_empty` 定义空结果的处理方案，你也可以在任何规则中使用 `empty` 表示一个空结果，就像下面这样：

```py
 def p_empty(p):
     'empty :'
     pass

 def p_optitem(p):
     'optitem : item'
     '        | empty'
     ...
```

还需要注意的是你定义的第一条规则将被默认作为顶级语法规则，你可以使用 `start` 对其进行修改，如：

```py
def p_foo(p):
    '''bar : A B'''

start = "foo"

# or 

parser = yacc.yacc(start="foo")
```

### 移入/规约

上面给出的语法规则是经过规约的规则，对解析器来说，它更容易处理，因为它几乎不存在歧义，但从编程的角度来说，我们可能会以一种更符合人类直觉的方式定义语法规则，就像下面这样：

```c
expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | LPAREN expression RPAREN
        | NUMBER
```

它如此简单，但存在大问题，考虑一个输入： `3+4*5`: 语法分析步骤如下：

```txt
Step  SymbolStack       Input Tokens    Action
-----------------------------------------------------------------------------
1     $                 3*4+5$          Shift 3
2     $3                 *4+5$          Redius: expr : NUMBER
3     $expr              *4+5$          Shift *
4     $expr *             4+5$          Shift 4
5     $expr * 4            +5$          Redius: expr : NUMBER
6     $expr * expr         +5$          !Shift + or Redius expr : expr * expr
```

当分析进行到第六步时，分析器不能确定应该是弹出 PLUS 还是对表达式 `expr * expr` 应用规则： `expr : expr * expr`,默认情况下，解析器会选择移入，即弹入 PLUS，这显然错了，因此我们需要指定规则的优先级：

```py
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)
```

`precedence` 中，TOKEN 优先级从小到大排列，上面的表达式声明了加减的优先级小于乘除，且它们都是左关联的。这些定义将被应用于每条语法规则，LR 语法中，语法规则的优先级总是由其最右面的富豪的优先级决定的。在进行语法分析时，将会按以下具体规则通过优先级解决冲突问题：

1. 如果当前 TOKEN 优先级小于堆栈上的优先级，进行规约，例如堆栈上是 `expr * expr` 优先级由 `*` 决定就是 2，当前 TOKEN 如果是 `+`, 优先级较小，就会对 `expr * expr` 进行规约
2. 如果当前 TOKEN 优先级高于堆栈上表达式优先级，将会进行移入操作，例如堆栈上是 `expr + expr` 优先级 1，当前 TOKEN 是 `*`, 那就会移入 `*` 得到 `expr + expr * `
3. 优先级相同的情况下对左关联进行规约，对右关联规则更改 TOKEN
4. 未设置优先级默认移入。

这里的一个漏洞是操作符在不同的上下文中可能有不同的优先级，考虑 `3 - 4 * -2` 其中的 `-` 在前面的用法中的优先级显然低于后面一个用法的优先级，为了解决这个问题，可以设置虚拟 TOKEN：

```py
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]
```

上面的例子中，设置了 UMINUS 的优先级最高，并在规则解析是，使用 `%prec UMINUS` 显式指定了规则使用的优先级是 `UMINUS`

还有一种冲突被称为 “规约/规约” 冲突，考虑以下语法规则：

```c
assigment : CHAR EQUALS NUMBER
          | CHAR EQUALS expression

expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | LPAREN expression RPAREN
        | NUMBER
```

当解析 `a=5` 时，我们应该应用 `assigment : CHAR EQUALS NUMBER` 还是 `assigment : CHAR EQUALS expression` 呢？当出现这种冲突时，yacc 会打印一下警告信息：

```txt
WARNING: 1 reduce/reduce conflict
WARNING: reduce/reduce conflict in state 15 resolved using rule (assignment -> ID EQUALS NUMBER)
WARNING: rejected rule (expression -> NUMBER)
```

上面的信息会告诉你发生了什么冲突，但并不会告诉你冲突是如何发生的，要了解语法分析的详细流程，你肯呢个需要阅读 `parser.out` 文件，该文件在语法分析器第一次运行时被生成，描述了语法分析的详细流程,文件内容其实很容易理解，你需要注意下面三点：

1. 文件中的每个 `state` 相当于语法分析的一个分支，里面描述了在这个状态下分析器允许输入的 TOKEN 或表达式，其中的 `.` 表示当前位置。
2. 解析器是依赖堆栈工作的，阅读时注意栈顶在靠右
3. 文件中用 `!` 标注出了冲突的地方，虽然这些冲突不见得都是不好的。

### 其他

一个良好的解析器不应该遇到错误就立刻返回，你应该尽可能返回所有的错误以便用户排查错误，你可以定义 `p_error` 来处理异常，它将以发生错误的 TOKEN 作为参数，在这里你可以做一些恢复错误的操作。

为了更好的追踪问题，打印错误位置是十分必要的,你可以在构建 parser 时指定 `tracking=True` 来追踪所有 TOKEN 的位置，当然，你也可以只追踪特定表达式特定 TOKEN 的位置：

```py
def p_expression(p):
     'expression : expression "+" expression'
     line   = p.lineno(2) # 追踪 + 的位置
     index  = p.lexpos(2)
```

## 后记

关于更详细的 ply 的用法参见官方文档，推荐一篇[文章](https://blog.csdn.net/qq_33414271/article/details/97686897?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-4-97686897-blog-79123776.pc_relevant_default&spm=1001.2101.3001.4242.3&utm_relevant_index=7)

最后附上上面例子中一个简单计算器的完整程序：

```py
import ply.lex as lex
import ply.yacc as yacc


class MyLexer:

    # reserved = {
    #     'if': 'IF',
    #     'then': 'THEN',
    #     'else': 'ELSE',
    #     'while': 'WHILE',
    # }
    # tokens = ("NUMBER", "CHAR") + tuple(reserved.values())
    tokens = ("NUMBER", "CHAR")
    literals = ['+', '-', '*', '/', '(', ')', '=']
    t_ignore = (" ")

    def __init__(self, **kwargs) -> None:
        self.lexer: lex.Lexer = lex.lex(module=self, **kwargs)

    def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CHAR(self, t: lex.LexToken) -> lex.LexToken:
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # t.type = self.reserved.get(t.value, 'CHAR')
        return t

    def t_error(self, t: lex.LexToken) -> lex.LexToken:
        print(f"Illegal character '{t.value}' in {t.lineno}:{t.lexpos}")
        t.lexer.skip(1)

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_expression_uminus(self, p):
        '''expression : "-" expression %prec UMINUS'''
        p[0] = -p[2]

    def p_assignment(self, p):
        '''assignment : CHAR "=" expression'''
        p[0] = p[3]

    def p_expression(self, p):
        '''expression : expression "+" expression
                      | expression "-" expression
                      | expression "*" expression
                      | expression "/" expression
                      | "(" expression ")"
                      | NUMBER'''
        if len(p) == 4:
            match p[2]:
                case "+":
                    p[0] = p[1] + p[3]
                case "-":
                    p[0] = p[1] - p[3]
                case "*":
                    p[0] = p[1] * p[3]
                case "/":
                    p[0] = p[1] / p[3]
        elif len(p) == 3:
            p[0] = [2]
        elif len(p) == 2:
            p[0] = p[1]

    def run(self, data):
        self.lexer.input(data)
        self.parser = yacc.yacc(module=self, start="assignment")
        result = self.parser.parse(data)
        print(result)


if __name__ == "__main__":
    data = "a=12+3 * 9 - 5*-3"
    lexer = MyLexer()
    lexer.run(data)

```
