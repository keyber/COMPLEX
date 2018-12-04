import math

def prime_test(N):
    """exponentiel"""
    racine = int(math.sqrt(N))
    for i in range(2,racine+1):
        if N%i==0:
            return False
    return True

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

assert my_expo_mod(12,[1,1],512) == 192

def test_fermat(nValue, nBinary, a):
    """return possiblement premier"""
    assert nValue>=2 and a>=2
    b = my_expo_mod(a, nBinary, nValue)
    return (b-a)%nValue == 0
    
#221 = 13*17
#221 est un pseudo premier en base 21,34,38,...
assert test_fermat(221,[1,1,0,1,1,1,0,1], 21)
assert test_fermat(221,[1,1,0,1,1,1,0,1], 34)
assert test_fermat(221,[1,1,0,1,1,1,0,1], 38)
assert not test_fermat(221,[1,1,0,1,1,1,0,1],37)


#2, 3 et 19 sont premiers
for _i in range(2,19):
    assert test_fermat(2, [1, 0], _i)
    assert test_fermat(3, [1, 1], _i)
    assert test_fermat(19,[1,0,0,1,1],_i)

#561 = 3 * 11 * 17 est un nombre de carmichael
for _i in range(3,561):
    assert test_fermat(561,[1,0,0,0,1,1,0,0,0,1],_i)

def error_proba(test, base):
    return sum((test_fermat(val, binary, base) for val, binary in test))/len(test)

def error_proba_detailed(test, base):
    err=0
    listErr=[0]*len(test)
    for i in range(len(test)):
        err += test_fermat(test[i][0], test[i][1],base)
        listErr[i]=err/(i+1)
    return listErr
    
def getBinary(n):
    """retourne l'écriture en base 2 du nombre n.
    res[0] est le MSB"""
    digits=[]
    while n:
        digits.append(n&1)
        n>>=1
    digits.reverse()
    return digits
    
def main():
    import matplotlib.pyplot as plt
    composed=[(i, getBinary(i)) for i in range(10**5) if not prime_test(i)]
    print("nombres composés considérés :",len(composed))
    #plt.figure()
    plt.plot(range(2,100), [error_proba(composed, base) for base in range(2, 100)])
    plt.xlabel("Base choisie")
    plt.ylabel("Probabilité d'erreur")
    plt.show()
    
main()