
def my_gcd(a, b):
    while b:
        a, b = b, a%b
    return a
#todo tests
def my_inverse(a, N):
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

from time import time
import matplotlib.pyplot as plt
import random
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
    """n en représentation binaire (n[0] est le LSB)"""
    h=1
    l = len(n)
    for i in range(l-1,-1,-1):
        h = (h*h)%N
        if n[i]==1:
            h=(h*g)%N
    return h

assert my_expo_mod(512,12,[1,1]) == 192


#EXERCICE 2
import math
def first_test(N):
    """soit n le nb de bit de N
    la taille de la représentation de sqrt(N) est en O(n/2) = O(n)
    il y a donc O(n) tours de boucle
    
    Si on considère que les opérations arithmétiques s'effectuent en O(1)
    alors la complexité est en O(n)
    Si elle est en O(bitsize(a) * bitsize(b))
    alors la complexité est
      O(n * n * bitsize(sqrt(N))) = O(n^3)
    """
    racine = int(math.sqrt(N))
    for i in range(2,racine+1):
        if N%i==0:
            return False
    return True

assert first_test(13)
assert not first_test(12)

def compte(N):
    return sum((first_test(i) for i in range(2, N)))

assert compte(100) == 25
assert compte(10) == 4
assert compte(10**5) == 9592

def carmichael(n):
    for a in range(n):
        #n divise a**(n-1) - 1
        if my_gcd(a, n) == 1 and not (a ** (n - 1) - 1) % n == 0:
            return False
    return True

def gen_carmichael(N):
    return [i for i in range(N) if carmichael(i)]

#print(gen_carmichael(10**3))
def gen_carmichael_3p():
    """boucle infinie
    n'a  l'air de rien trouver"""
    facteursPrem=[2,3,5]
    prod = 2*3*5
    n=6
    ind = 0
    while 1:
        if first_test(n):
            prod = prod // facteursPrem[ind] * n
            facteursPrem[ind] = n
            ind = (ind+1)%3
            if carmichael(prod):
                print(prod, facteursPrem)
        n+=1


def gen_carmichael_3p2():
    import itertools
    facteursPrem=[2,3]
    n=4
    while 1:
        if first_test(n):
            for f0,f1 in itertools.combinations(facteursPrem,2):
                prod = f0*f1*n
                if carmichael(prod):
                    print(prod, f0,f1,n)
            facteursPrem.append(n)
        n+=1
#gen_carmichael_3p2()

def test_3p_carmichael(p,q,r):
    if p==q or p==r or q==r:
        return False
    prod_moins1 = p*q*r - 1
    return prod_moins1 % (p-1) == 0 and \
           prod_moins1 % (q-1) == 0 and \
           prod_moins1 % (r-1) == 0

assert test_3p_carmichael(13, 37, 61)
