import math
import random


def my_expo_mod(g,n,N):
    """n en représentation binaire (n[0] est le MSB)
    retourne g**n % N
    polynomial"""
    h = 1
    for digit in n:
        h = h * h % N
        if digit:
            h = h * g % N
    return h


def test_miller_rabin(n, h, m, T):
    """n = 1 + 2**h * m
    m sous la forme de sa représentatiton binaire
    T nombre d'itération
    retourne possible premier"""
    for i in range(1,T):
        a = random.randint()#inversible modulo n
        b = my_expo_mod(a,m,n)
        if b!=1 and b!=n-1:
            for j in range(1,h-1):
                if b!=n-1 and b*2%n==1:
                    return 0
                b*=b
            if b != n-1:
                return 0
    return 1

def prime_test(N):
    """exponentiel"""
    racine = int(math.sqrt(N))
    for i in range(2, racine + 1):
        if N % i == 0:
            return False
    return True


#221 = 13*17
#221 est un pseudo premier en base 21,34,38,...
assert test_miller_rabin(221, [1, 1, 0, 1, 1, 1, 0, 1], 21)
assert test_fermat(221, [1, 1, 0, 1, 1, 1, 0, 1], 34)
assert test_fermat(221, [1, 1, 0, 1, 1, 1, 0, 1], 38)
assert not test_fermat(221, [1, 1, 0, 1, 1, 1, 0, 1], 37)

#2, 3 et 19 sont premiers
for _i in range(2, 19):
    assert test_fermat(2, [1, 0], _i)
    assert test_fermat(3, [1, 1], _i)
    assert test_fermat(19, [1, 0, 0, 1, 1], _i)

#561 = 3 * 11 * 17 est un nombre de carmichael
for _i in range(3, 561):
    assert test_fermat(561, [1, 0, 0, 0, 1, 1, 0, 0, 0, 1], _i)


def error_proba(test, base):
    return sum((test_fermat(val, binary, base) for val, binary in test)) / len(test)


def error_proba_detailed(test, base):
    err = 0
    listErr = [0] * len(test)
    for i in range(len(test)):
        err += test_fermat(test[i][0], test[i][1], base)
        listErr[i] = err / (i + 1)
    return listErr



def main():
    import matplotlib.pyplot as plt
    composed = [(i, getBinary(i)) for i in range(10 ** 5) if not prime_test(i)]
    print("nombres composés considérés :", len(composed))
    """for base in range(2,10):
        l = error_proba_detailed(composed, base)
        if max(l)<.1:
            print(base)"""
    #plt.figure()
    plt.plot(range(2, 100), [error_proba(composed, base) for base in range(2, 100)])
    plt.xlabel("Base choisie")
    plt.ylabel("Probabilité d'erreur")
    plt.show()


main()