Account = {balance = 0}
function Account.withdraw(v)
    Account.balance = Account.balance - v
end

-- class demo

Shape = {area=0}

function Shape:new(o, side)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    side = side or 0
    self.area = side * side
    return o
end

function Shape:printArea()
    print('面积 ', self.area)
end

myshape = Shape:new(nil, 10)
myshape:printArea()

Rectange = Shape:new()

function Rectange:new(o, length, width)
    o = o or Shape:new(o)
    setmetatable(o, self)
    self.__index = self
    self.area = length * width
    return o
end

function Rectange:printArea ()
    print("矩形面积为 ",self.area)
end

myrectange = Rectange:new(nil, 10, 20)
myrectange:printArea()