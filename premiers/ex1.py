from time import time
import matplotlib.pyplot as plt
import random

def my_gcd(a, b):
    """polynomial"""
    while b:
        a, b = b, a%b
    return a
assert my_gcd(10,5)==5
assert my_gcd(10,11)==1

def my_inverse(a, N):
    """polynomial"""
    if N==0:
        raise ArithmeticError(str(a) + "pas inversible modulo 0")
        
    u0, v0, r0 = 1, 0, a
    u1, v1, r1 = 0, 1, N
    while r1!=0:
        q = r0//r1
        u2,v2,r2 = u0-q*u1, v0-q*v1, r0-q*r1
        u0, v0, r0 = u1, v1, r1
        u1, v1, r1 = u2, v2, r2
        
    if r0==1:
        return u0 % N
    
    raise ArithmeticError(str(a) + " et " + str(N) + " pas inversibles")

assert my_inverse(5,4) == 1
assert my_inverse(16,9) == 4
try:
    my_inverse(10,12)
    assert False
except ArithmeticError:
    pass

def mesureCompGCD():
    l = []
    res = []
    x = [10,100,500,1000,1500,2000, 3000, 5000, 10000]
    for i in x:
        N=10**i
        t = time()
        for _ in range(100):
            a = random.randint(0,N)
            b = random.randint(0,N)
            res.append(my_gcd(a,b))
        l.append((time()-t)/100)
    plt.xlabel("N (échelle logarithmique)")
    plt.ylabel("Complexité (temps en secondes)")
    plt.plot(x,l)
    plt.show()
    print(res)

def mesureCompInv():
    l = []
    res = []
    x = [10,100,500,1000,1500,2000, 3000, 5000, 10000]
    for i in x:
        N = 10 ** i
        t = time()
        for _ in range(100):
            a = random.randint(0, N)
            b = random.randint(1, N)
            try:
                res.append(my_inverse(a,b))
            except ArithmeticError:
                pass
        l.append((time() - t) / 100)
    plt.xlabel("N (échelle logarithmique)")
    plt.ylabel("Complexité (temps en secondes)")
    plt.plot(x, l)
    plt.show()

def my_expo_mod(N,g,n):
    """n en représentation binaire (n[0] est le LSB)
    polynomial"""
    h = 1
    l = len(n)
    for i in range(l-1,-1,-1):
        h = h * h % N
        if n[i] == 1:
            h = h * g % N
    return h

assert my_expo_mod(512,12,[1,1]) == 192