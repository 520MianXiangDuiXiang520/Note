function fib(n)
    if n < 2 then
        return n
    else
        return fib(n - 1) + fib(n-2)
    end
end

function loop(n)
    for i = 1,n do
        print(i)
    end
end


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

-- Set()
-- Get()
-- Foreach()

--------------

Array = {1, 2, 3, 4, "Lua"}

function ForeachArray()
    for idx, v in pairs(Array) do
        print(k, v) -- 索引从 1 开始
    end
end

-- ForeachArray()

-- print(table.concat({1,2,3,4,5,6}, "-", 2, 4))

-- print(fib(0))
-- print(fib(1))
-- print(fib(3))
-- print(fib(4))
-- print(fib(5))
-- loop(10)


function sum(...)
    n = select("#", ...)
    res = 0
    for i = 1,n do
        print(select(i, ...))
        print((select(i, ...)))
        res = res + (select(i, ...))
    end
    return res
end

print(sum(1,2,3,4,5))