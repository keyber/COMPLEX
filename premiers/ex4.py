import math
import random

def my_expo_mod(g, n, N):
    """n en représentation binaire (n[0] est le MSB)
    retourne g**n % N
    polynomial"""
    h = 1
    for digit in n:
        h = h * h % N
        if digit:
            h = h * g % N
    return h


def prime_test(N):
    """exponentiel"""
    racine = int(math.sqrt(N))
    for i in range(2, racine + 1):
        if N % i == 0:
            return False
    return True


def my_gcd(a, b):
    """polynomial"""
    while b:
        a, b = b, a % b
    return a


def getBinary(n):
    """retourne l'écriture en base 2 du nombre n.
    res[0] est le MSB"""
    digits = []
    while n:
        digits.append(n & 1)
        n >>= 1
    digits.reverse()
    return digits

def get_hm_form(n):
    n -= 1
    h = 0
    while n & 1 == 0:
        n >>= 1
        h += 1
    return h, n

for _n in [11, 15, 4999]:
    _h, _m = get_hm_form(_n)
    assert 1 + 2 ** _h * _m == _n


def get_hm_formBinary(n):
    h,m = get_hm_form(n)
    return h, getBinary(m)


def test_miller_rabin(n, T):
    h,m = get_hm_formBinary(n)
    """h = 0
    m = n - 1
    while m % 2 == 0:
        m >>= 1
        h += 1
    assert (2 ** h * m == n - 1)"""

    for _ in range(T):#nombre de tours
        
        #base aléatoire
        a = random.randint(2, n-1)
        
        #calcul de a**m % n
        b = my_expo_mod(a, m, n)#b = pow(a, m, n)
        
        if b != 1 and b != n - 1:
            j=1
            while j<h and b!=n-1:
                b=b*b%n
                if b == 1:
                    return 0
                j+=1
            if b != n - 1:
                return 0
    
    #on n'a jamais trouvé de diviseur donc on retourne "premier"
    return 1


for _i in range(5,1000,2):
    if prime_test(_i):
        assert test_miller_rabin(_i, 1)
    
#221 = 13*17 = 1 + 4 * 55 = 1 + 2**2 * 55
assert not test_miller_rabin(221, 100)

#561 = 3 * 11 * 17 est un nombre de carmichael
#    = 1 + 2**4 * 35
#assert not test_miller_rabin(561, 4, [1, 0, 0, 0, 1, 1], 10)
assert not test_miller_rabin(561, 100)

#19 = 1 + 2**1 * 9   premier
#assert test_miller_rabin(19, 1, [1, 0, 0, 1], 10)
assert test_miller_rabin(19, 100)


def error_proba(test, T):
    return sum(test_miller_rabin(n, T) for n in test)/len(test)


def gen_rsa(t):
    m = 2**(t-1)
    M = 2*m
    
    p=random.randint(m,M)
    while not test_miller_rabin(p, 100):
        p = random.randint(m, M)
        
    q=random.randint(m,M)
    while q==p or not test_miller_rabin(q, 100):
        q = random.randint(m, M)

    return p*q,p,q

for _i in range(3,10):
    _n,_p,_q = gen_rsa(_i)
    assert prime_test(_p) and prime_test(_q) and not prime_test(_n)

def main():
    import matplotlib.pyplot as plt
    print("rsa ",gen_rsa(64))
    
    
    #s=10**5 #shift
    s=0 #shift
    
    composed = [i for i in range(s+1,s + 10**5,2) if not prime_test(i)]
    print("nombres composés considérés :", len(composed))
    
    r = range(1,5)
    redo=9
    err = [sum(error_proba(composed, T) for _ in range(redo))/redo for T in r]
    errMin = max(min(err),1e-9)
    print([x/errMin*100 for x in err])
    plt.plot(r, err)
    
    plt.xlabel("Nombre d'itérations T")
    plt.ylabel("Probabilité d'erreur")
    plt.show()


main()
