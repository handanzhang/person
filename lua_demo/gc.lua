collectgarbage('stop')

collectgarbage('collect')

local before = collectgarbage('count')

for i = 1, 10000 do
    local string = '100000000000000000000' .. '0'
end

local after = collectgarbage('count')

print('short same mem cost: ' .. (after - before) .. 'K')


local before = collectgarbage('count')

for i = 1, 10000 do
    local s = '1000000000000000000000000000000000000000000000000000000000000000000000000000000000' .. '0'
end

local after = collectgarbage('count')

print('long same mem cost: ' .. (after - before) .. 'K')