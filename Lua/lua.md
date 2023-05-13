# Lua

## 运行

```sh
lua HelloLua.lua 
# 或
luac HelloLua.lua
lua luac.out
```

## 语法

### 基本语法

```lua
-- 全局
v = 100

-- 局部
local v = 100
```

方法：

```lua
function fib(n)
    if n < 2 then
        return n
    else
        return fib(n - 1) + fib(n-2)
    end
end

print(fib(0))
print(fib(1))
print(fib(3))
print(fib(4))
print(fib(5))

-- select 可变参函数
function sum(...)
    n = select("#", ...) -- 取可变参长度
    res = 0
    for i = 1,n do
        print(select(i, ...)) -- 可变参数从 i 开始
        print((select(i, ...))) -- 多加了一层括号，指取第一个
        res = res + (select(i, ...))
    end
    return res
end

print(sum(1,2,3,4,5))

-- 1       2       3       4       5
-- 1
-- 2       3       4       5
-- 2
-- 3       4       5
-- 3
-- 4       5
-- 4
-- 5
-- 5
-- 15
```

pack h和 unpack

流程控制：

```lua
function loop(n)
    for i = 1,n do
        print(i)
    end
end

function fib(n)
    if n < 2 then
        return n
    else
        return fib(n - 1) + fib(n-2)
    end
end
```

### 数据结构

#### Table

用作字典：

```lua
Char = {Name="Q", Addr="w"}

function Set()
    Char.Id = 1
    Char["Type"] = "Square"
end

function Get()
    print(Char.Name, Char.Addr, Char.Id, Char.Type)
end

function Foreach()
    for k, v in pairs(Char) do
        print(k, v)
    end
end

Set()
Get()
Foreach()
```

用作数组

```lua
Array = {1, 2, 3, 4, "Lua"}

function ForeachArray()
    for idx, v in pairs(Array) do
        print(k, v) -- 索引从 1 开始
    end
end

ForeachArray()
```

Table Api:
1. `table.concat(table, [sep, start, end])`: 连接 Table 中的元素，  sep 默认空字符串，start 默认 1 end默认长度，如
   ```lua
      print(table.concat({1,2,3,4,5,6}, "-", 2, 4)) -- 2-3-4
   ```
2. `table.insert(table, [pos], value)`: 插入元素，pos 默认 size + 1
3. `table.maxn(table)`: 最大正数索引（长度），O(n) 复杂度
4. `table.remove(table, [pos])`: 删除
5. `table.sort(table, [comp])`: 排序， comp 是一个比较函数

## OOP

