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


assert my_gcd(10, 5) == 5
assert my_gcd(10, 11) == 1


def test_miller_rabin_BAD(n, T):
    """n = 1 + 2**h * m
    m sous la forme de sa représentatiton binaire
    T nombre d'itération
    retourne possible premier"""
    h = 0
    m = n - 1
    while m % 2 == 0:
        m >>= 1
        h += 1
    assert (2 ** h * m == n - 1)

    for i in range(T):
        #a aléatoire inversible modulo n
        a = random.randint(2, n-1)
        while my_gcd(a, n) != 1:
            a = random.randint(2, n-1)
        
        #b = my_expo_mod(a, m, n)
        b = pow(a, m, n)
        
        if b != 1 and b != n - 1:
            for _ in range(h-1):
                if b != n - 1 and b*b % n == 1:
                    return 0
                b = b*b%n
            if b != n - 1:
                return 0
    return 1


def test_miller_rabin(n, T):
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)
    
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True
    
    for _ in range(T):
        a = random.randint(2, n-1)
        if trial_composite(a):
            return False
    
    return True

for _i in range(5,1000,2):
    if prime_test(_i):
        assert test_miller_rabin(_i, 1)
        
#221 = 13*17 = 1 + 4 * 55 = 1 + 2**2 * 55
#assert not test_miller_rabin(221, 2, [1, 1, 0, 1, 1, 1], 10)
assert not test_miller_rabin(221, 10)

#19 = 1 + 2**1 * 9   premier
#assert test_miller_rabin(19, 1, [1, 0, 0, 1], 10)
assert test_miller_rabin(19, 10)

#561 = 3 * 11 * 17 est un nombre de carmichael
#    = 1 + 2**4 * 35
#assert not test_miller_rabin(561, 4, [1, 0, 0, 0, 1, 1], 10)
assert not test_miller_rabin(561, 10)


def error_proba(test, T):
    return sum(test_miller_rabin(n, int(T)+(random.random()<T-int(T))) for n in test)/len(test)

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

def main():
    import matplotlib.pyplot as plt
    s=0#10**10 #shift
    composed = [i for i in range(s+1,s + 10**5,2) if not prime_test(i)]
    print("nombres composés considérés :", len(composed))
    
    
    r = [1+i*.2 for i in range(15)]
    print(r)
    err = [error_proba(composed, T) for T in r]
    errMin = max(min(err),1e-9)
    print([x/errMin*100 for x in err])
    plt.plot(r, err)
    
    plt.xlabel("Nombre d'itérations T")
    plt.ylabel("Probabilité d'erreur")
    plt.show()


main()
