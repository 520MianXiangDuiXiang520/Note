# 上帝的编程语言 Lisp

Lisp 是世界上第二古老的编程语言，但直到今天，在 tiobe 的排行榜上，它仍排名 27，占有率 0.49% 甚至高于 Lua(29 0.44%) 和 Kotlin(33 0.37%)， 有人说它是上帝的编程语言，在 《漫画家与黑客》中，保罗格雷厄姆说：最后真正非常严肃地把黑客作为人生目标的人，应该考虑学习 Lisp。

## Hello World

Lisp 有许多变种的方言，我们选择 clisp：

```sh
brew install clisp
```

之后执行 clisp 就可以进入交互环境了, 也可以 `clisp 文件名`  来执行：

```lisp
(pprint "hello lisp")
```


