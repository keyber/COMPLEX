import numpy as np
import sys

N = 0    #le nombre d'objets
B = 0    #la capacité du sac à dos, fixé à total/2
U = None #l'utilité: quelconque
P = None #le poids: positif non nul entier
Q = None #le rendement des objets = U/P


def instance(n, classe, R):
    """selon classe:
    0) p u indépendant ~ U[1,R]
    1) p ~ U[1,R] u ~ U[p-R/10, p+R/10]
    2) p = u ~ U[1,R]
    return u, p"""
    from random import randint
    global N,B
    if classe==0:
        p = [randint(1,R) for _ in range(n)]
        u = [randint(1,R) for _ in range(n)]
    elif classe==1:
        p = [randint(1,R) for _ in range(n)]
        u = [randint(i-R//10, i+R//10) for i in p]
    else:
        p = [randint(1,R) for _ in range(n)]
        u = p #dupliqués en passant par np.array
    N = n
    B = sum(p)//2
    return np.array(u), np.array(p)

def ini(u,p):
    global U,P,Q
    U = np.array(u)
    P = np.array(p)
    try:
        Q = U/P
    except RuntimeWarning:
        print(P)

    #tri par Q décroissant
    sortedIndexes = np.argsort(Q)
    U = U[sortedIndexes]
    P = P[sortedIndexes]
    Q = Q[sortedIndexes]

    return sortedIndexes

def gloutonEntier(ind, u, p):
    """ind: indices dispo
    u: utilité actuelle
    p: poids restant
    return u atteinte, indices pris, poids restant"""
    res = []
    for i in ind:
        if P[i]<=p:
            p-=P[i]
            u+=U[i]
            res.append(i)
            if p==0:
                break
    return u, res, p

def gloutonPartie(ind, u, p):
    """ind: indices dispo
    u: utilité actuelle
    p: poids restant
    return u atteinte"""
    for i in [i for i in ind if P[i]<=p]:
        if P[i]<p:
            p-=P[i]
            u+=U[i]
        else:
            u+=U[i]*p/P[i]
            break
    return u

class Noeud:
    def __init__(self,depthRestante, index, utilite, poidsRestant, borne):
        self.d = depthRestante
        self.ind = index
        self.u = utilite
        self.p = poidsRestant
        self._childs = 2 if self.d>0 else 0
        self.borne=borne

    @classmethod
    def racineMin(cls, depth, poids):
        return cls(depth, [], 0, poids, -1 << 31)

    @classmethod
    def racineMax(cls, depth, poids):
        return cls(depth, [], 0, poids, 1 << 31)

    def realisable(self):
        return self.p>=0

    def hasNext(self):
        return self._childs

    def next(self):
        """return le noeud suivant
        pourrait etre fait en O(1)"""
        
        self._childs -= 1
        
        if self._childs==1:
            #prend l'objet suivant: ajoute l'indice à une copie de la liste, poids et valeur
            ind2 = self.ind.copy()#O(n)
            ind2.append(self.d-1)
            return Noeud(self.d-1,ind2, self.u+U[self.d-1],self.p-P[self.d-1],self.borne)
        
        #ne prend pas
        return Noeud(self.d-1, self.ind, self.u, self.p,self.borne)

    def eval(self):
        return self.u

def naif():
    """return indices d'une sol opti, valeur, poids restant, nbNoeud"""
    cpt=0
    u = 0
    pile = [Noeud.racineMax(N,B)]
    ind=[]
    p=0
    while len(pile):
        n = pile[-1]
        
        #évalue feuille
        if n.realisable() and n.d==0:
            e = n.eval()
            if e>u:
                ind=n.ind
                u=n.u
                p=n.p
        
        #ajoute fils
        if n.realisable() and n.hasNext():
            pile.append(n.next())
        #fin branche
        else:
            pile.pop()
            cpt+=1
        
    return ind,u,p,cpt

def branchBound():
    """return indices d'une sol opti, valeur, poids restant nbNoeud"""
    cpt=0
    pile = [Noeud.racineMax(N,B)]
    inf = 0#correspond à l'utilité
    resInd=None  # type: list
    resP=0
    remonte=False
    while len(pile):
        n = pile[-1]
        #évaluation
        if not remonte and n.realisable():
            #noeud intermédiaire
            if n.hasNext():
                u,ind,p = gloutonEntier(range(n.d-1,-1,-1), n.u, n.p)
                ind = n.ind + ind
            #feuille
            else:
                ind=n.ind
                u=n.u
                p=n.p
            
            #mise à jour meilleur solution
            if u>inf:
                inf=u
                resInd=ind
                resP=p
        
        finBranche = False
        
        # fin si not réa | feuille
        if not n.realisable() or not n.hasNext():
            finBranche = True
        
        # fin si élague
        if n.realisable() and n.hasNext():
            if not remonte:#quand on remonte, la borne sup ne peut pas changer
                n.borne = min(n.borne, gloutonPartie(range(n.d-1,-1,-1), n.u, n.p))
            #la borne inf a pu atteindre la borne sup
            finBranche = finBranche or inf >= n.borne
        
        if finBranche:
            pile.pop()
            cpt+=1
            remonte=True
        else:#ajoute fils
            pile.append(n.next())
            remonte=False
    
    return resInd,inf,resP,cpt

import matplotlib.pyplot as plt

def main():
    from time import time
    #len(sys.argv)==4:
    #u,p = instance(*map(int,sys.argv[1:]))
    
    aff=[]
    print("n, nbnoeuds, std, temps, std")
    for n in [100*i for i in range(1,11)]:
        L=[]
        for i in range(10):
            u,p = instance(n,0,10000)
            t = time()
            sortedIndexes = ini(u,p)
            #a,b,c,d = naif()
            a,b,c,d = branchBound()
            L.append([a,b,c,d,time()-t])
        
        L=np.array(L)
        print(N, np.mean(L[:,3]), np.std(L[:,3]), np.mean(L[:,4]), np.std(L[:,4]))
        aff.append([N, np.mean(L[:,3]), np.std(L[:,3]), np.mean(L[:,4]), np.std(L[:,4])])
    
    aff = np.array(aff)
    plt.errorbar(aff[:,0], aff[:,1], aff[:,2])
    plt.title("noeuds")
    plt.figure()
    plt.title("temps")
    plt.errorbar(aff[:,0], aff[:,3], aff[:,4])
    plt.show()
    #a,b,c = plt.hist(l,bins=range(1,N+1))
    #print(a,b,c)
    #plt.show()

main()