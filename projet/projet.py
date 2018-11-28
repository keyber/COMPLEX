
def my_gcd(a, b):
    while b:
        a, b = b, a%b
    return a
assert my_gcd(10,5)==5
assert my_gcd(10,11)==1

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

assert my_inverse(5,4) == 1
assert my_inverse(16,9) == 4
try:
    my_inverse(10,12)
    assert False
except ArithmeticError:
    pass


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
    h = 1
    l = len(n)
    for i in range(l-1,-1,-1):
        h = h * h % N
        if n[i] == 1:
            h = h * g % N
    return h

assert my_expo_mod(512,12,[1,1]) == 192


#EXERCICE 2
import math
def first_test(N):
    """exponentiel car 2^(n/2) itérations"""
    racine = int(math.sqrt(N))
    for i in range(2,racine+1):
        if N%i==0:
            return False
    return True

assert first_test(2)
assert first_test(13)
assert not first_test(12)

def gen_primes(n):
    """nombre exponentiel d'appels à une fonction de coût exponentiel"""
    return [i for i in range(2, n) if first_test(i)]

PRIMES = gen_primes(10**5)
assert gen_primes(15) == [2,3,5,7,11,13]
assert len(gen_primes(100)) == 25
assert len(PRIMES) == 9592

def prime_factorization(n, primes):
    """retourne la décomposition en produit de facteurs premiers de n sous la forme
    d'un tableau des puissances des nombres premiers
    prend en paramètre la liste des nombres premiers inférieurs à n"""
    res = [0]
    i = 0
    while primes[i]<=n:
        if n%primes[i]==0:
            res[i]+=1
            n=n//primes[i]
        else:
            i+=1
            res.append(0)#puissance pour le prochain nombre premier
    
    return res

assert prime_factorization(1, PRIMES) == [0]
assert prime_factorization(2, PRIMES) == [1]
assert prime_factorization(3, PRIMES) == [0, 1]
assert prime_factorization(8, PRIMES) == [3]
assert prime_factorization(14, PRIMES) == [1,0,0,1]

def test_carmichael(n, primes):
    """implémentation par le critère de Korselt :
    carmichael <=> composé et square free et pour tout diviseur premier p on a: p-1|n-1"""

    #calcule sa décomposition en produit de facteurs premiers
    puissances = prime_factorization(n, primes)
    
    distincts = 0
    for i in range(len(puissances)):
        #square free
        if puissances[i]:
            if puissances[i]>1:
                return False
        
            #p-1|n-1
            if (n - 1) % (primes[i] - 1) != 0:
                return False
            distincts += 1
    
    #composé
    if distincts < 2:
        return False
    
    return True

assert not test_carmichael(7, PRIMES)
assert not test_carmichael(61, PRIMES)
assert not test_carmichael(562, PRIMES)
assert test_carmichael(561, PRIMES)
assert test_carmichael(2465, PRIMES)


def gen_carmichael(N, primes):
    """exponentiel car boucle de 1 à N"""
    return [i for i in range(1, N) if test_carmichael(i, primes)]

assert gen_carmichael(10**4, PRIMES) == [561,1105,1729,2465,2821,6601,8911]
#CARMI = gen_carmichael(10**5, PRIMES)
#assert len(CARMI)==16


def test_3p_carmichael(p,q,r):
    """critère de Korselt"""
    if p==q or p==r or q==r:#square free
        return False
    prod_moins1 = p*q*r - 1
    return prod_moins1 % (p-1) == 0 and \
           prod_moins1 % (q-1) == 0 and \
           prod_moins1 % (r-1) == 0

assert test_3p_carmichael(3,11,17)
assert not test_3p_carmichael(5,11,17)
assert test_3p_carmichael(5,13,17)
#nombre maximal obtenu en 5 minutes sans utiliser le critère de Korselt :
assert test_3p_carmichael(13, 37, 61)

def gen_carmichael_3p():
    """boucle infinie
    affiche les résultats trouvés au fur et à mesure"""
    #liste des nombres premiers inférieurs à n
    facteursPrem=[2,3]
    n=4
    while 1:
        if first_test(n):
            #cherche les nombre de carmichael qui sont le produit de n
            #et deux autres nombres premiers distincts strictement inférieurs à n
            
            #pour chaque combinaison de 2 nombres parmi la liste des facteurs premiers
            for i in range(len(facteursPrem)):
                f0 = facteursPrem[i]
                for f1 in facteursPrem[f0:]:
                    
                    #teste si le produit de ces deux nombres avec n est un nombre de carmichael
                    if test_3p_carmichael(f0,f1,n):
                        print(f0*f1*n,"=", f0,"*",f1,"*",n)
            
            #ajoute n à la liste des nombres premiers
            facteursPrem.append(n)
        n+=1
        


def gen_carmichael_1_2p(r):
    """retourne l'ensemble (fini) des nombres de carmichael de la forme
    p*q*r avec r fixé"""
    assert first_test(r)
    
    def f(r, x):
        return (x * r - 1) // (x - 1)
    
    inf = r*r
    sup = f(r, 2) * f(r, 3)#optimisable (par exemple en f(r,3)*f(r,5))
    
    list_ab=[]
    #on énumère tous les couples (a,b) dont le produit est entre inf et sup (strictement)
    #avc a<b et a et b premiers
    for produit in range(inf+1, sup):
        for a in range(2,int(math.sqrt(produit))+1):
            if produit%a==0:
                list_ab.append((a, produit//a))
    
    def pq_from_ab(a, b):
        p = (r * (b - 1) + b * (a - 1)) // (a * b - r * r)
        q = (1 + a * (p - 1)) // r
        return p, q
    
    #on détermine p et q à partir de a et b pour chaque couple
    ens_pq = {pq_from_ab(a,b) for a,b in list_ab}
    
    #restreint à l'ensemble des p et q premiers et p*q*r nombre de carmichael
    carmi = [(p,q) for p,q in ens_pq if
            test_3p_carmichael(r,p,q) and first_test(p) and first_test(q)]
    
    #retourne la liste triée par produit croissant
    return sorted(carmi, key=lambda x : x[0]*x[1])

def print1_2(r, carmi_1_2p):
    print("\nNombres de Carmichael de la forme pqr avec r =",r)
    for p,q in carmi_1_2p:
        print(r*p*q, "=", r,"*",p,"*",q)
    print()

print1_2(3, gen_carmichael_1_2p(3))
print1_2(5, gen_carmichael_1_2p(5))

print("tout :")
gen_carmichael_3p()
