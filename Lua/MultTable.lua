-- Demo1:  九九乘法表
-- Date:   2021/05/11 11:00
-- Author: Junebao

for i = 1, 9 do
    local line = ""
    for j = i, 9 do
        res = i * j

        line = line .. i .. " * " .. j .. " = " .. res .. "  "
    end
    print(line)
end