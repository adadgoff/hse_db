import itertools

n = 3
q = itertools.islice(itertools.product((1, 2), ('a', 'b', 'c')), n)

print(*q)
