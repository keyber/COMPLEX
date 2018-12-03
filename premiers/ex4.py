import random
from ex1 import my_gcd
from ex2 import prime_test

def test_miller_rabin(h,m,T):
    n=1+(2**h)*m
    print(n)
    for i in range (1,T+1):
        a=random.randint(1,n)
        while (my_gcd(a,n)!=1):
            a=random.randint(1,n)
        b=a**m%n
        if b!=1 and b!=n-1:
            for j in range(1,h):
                
                if b!=n-1 and b*b%n==1:
                    return "Compose"
                b=b*b%n
            if b!=n-1:
                return "Compose"
    return "Premier"

#1+(2**2)*4=17
assert test_miller_rabin(2,3,100)=="Premier"

#561 = 3 * 11 * 17 est un nombre de carmichael
#561 = 1+2**4*35
print(test_miller_rabin(4,35,100))

#1+(2**2)*5=21
print(test_miller_rabin(2,5,100))

#h1=random.randint(1,10)
#m1=random.randint(1,10)
#print(test_miller_rabin(h1,m1,100))

#Genere une liste de couple (h,m) tel que 1+2**h*m <=max avec m impair
def gen_list(max):
    h=1
    res=[]
    while (1+2**h<=max):
        m=1
        while (1+2**h*m<=max):
            res.append((h,m))
            m+=2
        h+=1
    return res

#print(gen_list(385))

def proba_erreur():
    erreura=0
    erreurb=0
    liste=gen_list(10000)
    for (k,l) in liste:
            n=1+2**k*l
            if (prime_test(n)):
                if (test_miller_rabin(k,l,100)=="Compose"):
                    erreura+=1
                    print("erreur a avec n=",n," il est premier")
                else :
                    print("c'est juste ",n)
            else:
                if (test_miller_rabin(k,l,100)=="Premier"):
                    erreurb+=1
                    print("erreur b avec n=",n," il est compose")
    taille=len(liste)
    print(erreura,erreurb,taille,erreurb/taille)
    
#proba_erreur()

def gen_rsa(t):
    liste=gen_list(2**t)
    for elem in liste:
        if (1+2**elem[0]*elem[1]<2**(t-1)):
            liste.remove(elem)
            
    (h,m)=liste[random.randint(0,len(liste))]
    while (test_miller_rabin(h,m,100)=="Compose"):
        (h,m)=liste[random.randint(0,len(liste))]
    p=1+2**h*m
    
    (h,m)=liste[random.randint(0,len(liste))]
    while (test_miller_rabin(h,m,100)=="Compose"):
        (h,m)=liste[random.randint(0,len(liste))]
    q=1+2**h*m
    
    print(p,q,p*q)
    return p*q

gen_rsa(12)
