Char = {
    Id = 0,
    Name = ""
}

function Char:new(id, name)
    self.Name = name
    self.Id = id
    return self
end


function Char:GetId()
    return self.Id
end

local c = Char:new(1, "w")
print(c.Name, c.Id)


------------------- square 

Square = {
    Age = 0
}
function Square:new(id, name, age)
    -- 访问 base 访问不到就找我
    -- local base = Char:new(id, name)
    -- self.Age = age
    -- setmetatable(base, self)
    -- self.__index = self
    -- return base

    -- 访问我，访问不到找 base
    
    local base = Char:new(id, name)
    self.Age = age
    setmetatable(self, base)
    base.__index = base

    return self
end

local sq = Square:new(199, "3", 9)
print(sq.Name, sq.Age)
print(sq:GetId())


-----------

-- a = {}

-- metaA = {}

-- setmetatable(a, metaA)

-- metaA.__index = {
--     Age = 10000
-- }

-- print(a.Age)
-- print(metaA.Age)

