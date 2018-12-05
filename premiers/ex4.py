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


def test_miller_rabin(n, T):
    h = 0
    m = n - 1
    while m % 2 == 0:
        m >>= 1
        h += 1
    assert (2 ** h * m == n - 1)

    for i in range(T):
        #a aléatoire inversible modulo n
        a = random.randint(2, n-1)
        
        #b = my_expo_mod(a, m, n)
        b = pow(a, m, n)
        
        if b != 1 and b != n - 1:
            j=1
            while j<h and b!=n-1:
                b=b*b%n
                if b == 1:
                    return 0
                j+=1
            if b != n - 1:
                return 0
    return 1

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


"""def test_miller_rabin(n, T):
    h, m = get_hm_formBinary(n)
    
    def strongTest(a):
        b = my_expo_mod(a, m, n)
        if b != 1 and b != n - 1:
            for _ in range(h - 1):
                b = b * b % n
                if b == 1:
                    return 0
                if b == n - 1:
                    return 1
        return 1
    
    for _ in range(T):
        a = random.randint(2, n-1)
        if not strongTest(a):#on a trouvé un diviseur
            return 0
        
    #on a jamais trouvé de diviseur
    return 1"""

for _i in range(5,1000,2):
    if prime_test(_i):
        assert test_miller_rabin(_i, 1)
    
#221 = 13*17 = 1 + 4 * 55 = 1 + 2**2 * 55
assert not test_miller_rabin(221, 100)

#19 = 1 + 2**1 * 9   premier
#assert test_miller_rabin(19, 1, [1, 0, 0, 1], 10)
assert test_miller_rabin(19, 10)

#561 = 3 * 11 * 17 est un nombre de carmichael
#    = 1 + 2**4 * 35
#assert not test_miller_rabin(561, 4, [1, 0, 0, 0, 1, 1], 10)
assert not test_miller_rabin(561, 100)


def error_proba(test, T):
    return sum(test_miller_rabin(n, T) for n in test)/len(test)

def main():
    import matplotlib.pyplot as plt
    #s=10**5 #shift
    s=0 #shift
    
    composed = [i for i in range(s+1,s + 10**5 * 2,2) if not prime_test(i)]
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
