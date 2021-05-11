cache = {}
function Fib(n)
    if (cache[n])
    then
        return cache[n]
    else
        if (n <= 2)
        then
            cache[n] = 1
            return 1
        else
            local res = Fib(n - 1) + Fib(n - 2)
            cache[n] = res
            return res
        end
    end
end


print(Fib(1)) -- 1
print(Fib(2)) -- 1
print(Fib(3)) -- 2
print(Fib(4)) -- 3
print(Fib(5)) -- 5
print(Fib(50))