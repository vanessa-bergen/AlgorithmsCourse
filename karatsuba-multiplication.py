"""
In this programming assignment you will implement one or more of the integer multiplication algorithms described in lecture.

To get the most out of this assignment, your program should restrict itself to multiplying only pairs of single-digit numbers.  You can implement the grade-school algorithm if you want, but to get the most out of the assignment you'll want to implement recursive integer multiplication and/or Karatsuba's algorithm.

So: what's the product of the following two 64-digit numbers?

3141592653589793238462643383279502884197169399375105820974944592

2718281828459045235360287471352662497757247093699959574966967627
"""

class Multiply(object):
    def karatsuba(self, x, y):
        if x < 10 or y < 10:
            return x * y

        # get the longest number of digits
        n = max(len(str(x)), len(str(y)))
        # if the number of digits is odd, substract 1
        n -= n % 2
        bn = 10 ** (n // 2)
        # if n is even, the number will get split in half ex: 1234 -> a = 12, b = 34
        # if n is odd, the second number will be greater ex: 123 -> a = 1, b = 23
        a, b = divmod(x, bn)
        c, d = divmod(y, bn)
        ac = self.karatsuba(a, c)
        bd = self.karatsuba(b, d)
        adbc = self.karatsuba(a + b, c + d) - ac - bd
        
        return ((10 ** n) * ac) + bn * adbc + bd

    
m = Multiply()
print(m.karatsuba(3141592653589793238462643383279502884197169399375105820974944592, 2718281828459045235360287471352662497757247093699959574966967627))

