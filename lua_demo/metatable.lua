window = {}

window.prototype = {x = 0, y = 0, width = 70, height = 70}

window.mt = {}

function window.new(o)
    setmetatable(o, window.mt)
    return o
end


window.mt.__index = function(table, key)
    return window.prototype[key]
end

w = window.new({x=10, y=20})
print(w.width)

print("---------- __newindex----------------")

t1 = {}

t = setmetatable({key1='value1'}, {__newindex= t1})

print(t.key1)

t.newkey = "新值2"

print(t.newkey, t1.newkey)

t.key1 = '新值1'

print(t.key1, t1.key1)


--[[ -
    __add +
    __sub -
    __mul *
    __div /
    __unm -
    __concat ..
    __eq     ==
    __mod    %
    __pow    ^
    __lt     <
-]]


t0 = setmetatable({10,20,30}, {
    __tostring = function(t)
        sum = 0
        for k, v in pairs(t) do
            sum = sum + v
        end

        return "元素和 " .. sum 
    end
})

print(t0)