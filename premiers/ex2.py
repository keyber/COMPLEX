import math

def prime_test(N):
    """exponentiel car 2^(n/2) itérations"""
    racine = int(math.sqrt(N))
    for i in range(2,racine+1):
        if N%i==0:
            return False
    return True

assert prime_test(2)
assert prime_test(13)
assert not prime_test(12)

def gen_primes(n):
    """nombre exponentiel d'appels à une fonction de coût exponentiel"""
    return [i for i in range(2, n) if prime_test(i)]

print("Calcul des nombres premiers...")
PRIMES = gen_primes(10**5)
print("Calcul des nombres premiers effectué")
assert gen_primes(15) == [2,3,5,7,11,13]
assert len(gen_primes(100)) == 25
assert len(gen_primes(10**5)) == 9592

def prime_factorization(n, primes):
    """retourne la décomposition en produit de facteurs premiers de n sous la forme
    d'une liste de couple (facteur premier, puissance)
    prend en paramètre la liste des nombres premiers inférieurs à n
    polynomial"""
    assert n!=0
    res = []
    i = 0
    
    #tant que n n'est pas complètement décomposé
    while n!=1:
        
        #le nombre premier courant divise n
        if n%primes[i]==0:
            #ajoute 1 à la puissance du nombre premier actuel
            if len(res) and res[-1][0]==primes[i]:
                res[-1][1]+=1
                
            #crée une case pour insérer cette nouvelle puissance
            else:
                res.append([primes[i],1])
            
            #continue avec le quotient de n par p
            n=n//primes[i]
        
        #on passe au nombre premier suivant
        else:
            i+=1
    
    return res

assert prime_factorization(1, PRIMES) == []
assert prime_factorization(2, PRIMES) == [[2,1]]
assert prime_factorization(3, PRIMES) == [[3,1]]
assert prime_factorization(8, PRIMES) == [[2,3]]
assert prime_factorization(14, PRIMES) == [[2,1],[7,1]]
assert prime_factorization(98, PRIMES) == [[2,1],[7,2]]

def test_carmichael(n, primes):
    """implémentation par le critère de Korselt :
    carmichael <=> composé et square free et pour tout diviseur premier p on a: p-1|n-1
    complexité polynomiale"""
    #calcule sa décomposition en produit de facteurs premiers
    decomposition = prime_factorization(n, primes)

    #composé
    if len(decomposition)<2:
        return False
    
    for facteur, puissance in decomposition:
        #square free
        if puissance>1:
            return False
        
        #p-1|n-1
        if (n - 1) % (facteur - 1) != 0:
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
#assert len(gen_carmichael(10**5, PRIMES))==16


def test_3p_carmichael(p,q,r):
    """critère de Korselt,
    p q et r doivent être des nombres premiers."""
    if p==q or p==r or q==r:#square free
        return False
    prod_moins1 = p*q*r - 1
    return prod_moins1 % (p-1) == 0 and \
           prod_moins1 % (q-1) == 0 and \
           prod_moins1 % (r-1) == 0

assert test_3p_carmichael(3,11,17)
assert not test_3p_carmichael(5,11,17)
assert test_3p_carmichael(5,13,17)
#nombre maximal obtenu en 5 minutes : 588909469501
assert test_3p_carmichael(1871, 16831, 18701)

def gen_carmichael_3p():
    """boucle infinie
    affiche les résultats trouvés au fur et à mesure"""
    #liste des nombres premiers inférieurs à n
    facteursPrem=[2,3]
    n=4
    while 1:
        if prime_test(n):
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

def nextPrimes(p, n):
    """renvoie les n nombres premiers consécutifs à p"""
    primes = []
    i = p + 1
    while len(primes) != n:
        if prime_test(i):
            primes.append(i)
        i += 1
    return primes


def gen_carmichael_1_2p(p):
    """retourne l'ensemble (fini) des nombres de carmichael de la forme
    p*q*r avec p fixé"""
    assert prime_test(p)
    
    p2, p3 = nextPrimes(p, 2)
    sup_h = (p*p2-1)*(p*p3-1)//((p2-1)*(p3-1)) #à multiplier par 1/h
    
    res = []
    for h in range(2,p):
        
        #détermine les bornes de recherche pour k
        inf = p*p//h + 1
        sup = sup_h//h
        for k in range(inf, sup+1):
            
            #calcule les valeurs de q et r correspondant aux valeurs de h et k
            q = (p+h) * (p-1) // (h*k - p*p) + 1
            r = (p*q - 1) // h + 1
            
            #si le nombre obtenu convient, l'ajoute au résultat
            if test_3p_carmichael(p,q,r) and prime_test(q) and prime_test(r):
                res.append((q,r))
                
    return res


def print1_2(p, carmi_1_2p):
    print("\nNombres de Carmichael de la forme p<q<r avec p =",p)
    for q,r in carmi_1_2p:
        print(p*q*r, "=", p,"*",q,"*",r)
    print()

def main():
    print(PRIMES[:100])
    CARMI = gen_carmichael(10**5, PRIMES)
    print(CARMI)
    assert len(CARMI) == 16
    
    for p in PRIMES[:6]:
        print1_2(p, gen_carmichael_1_2p(p))
    
    print("forme pqr :")
    gen_carmichael_3p()

#main()
