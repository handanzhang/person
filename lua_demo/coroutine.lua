function foo(a)
	print('foo �������' , a)
	return coroutine.yield(2 * a)
end

co = coroutine.create(function(a, b)
	print('��һ��Эͬ���', a, b)
	local r = foo(a+1)

	print('�ڶ���Эͬ���', r)
	local r, s = coroutine.yield(a+b, a -b)

	print('������Эͬ���', r, s)

	return b, '����Эͬ����'

end)


print('main', coroutine.resume(co, 1, 10))

print('main', coroutine.resume(co, 'r'))

print('main', coroutine.resume(co, 'x', 'y'))

print('main', coroutine.resume(co, 'x', 'y'))
