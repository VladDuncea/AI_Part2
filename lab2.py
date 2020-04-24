#EX 2a
a = [12,22,431,120,99,983,23,2234,1,10]
a = sorted(a, key=lambda x: str(x))
print(a)

#EX 2b
a = [12,22,431,120,99,983,23,2234,1,10]
a = sorted(a, key=lambda x: (x % 10, (x % 100)/10))
print(a)

#EX 2c
a = [12,22,431,120,99,983,23,2234,1,10]
a = sorted(a, key=lambda x: len(str(x)))
print(a)

#EX 2d
a = [12,22,431,120,99,983,23,2234,1,10]
a = sorted(a, key=lambda x: len(set(str(x))))
print(a)