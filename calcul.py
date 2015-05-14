#definition d'un fontion pour les Combinaison de C
from molecule import *
from random import randrange

def UneChaineCarbonnee (nbCarbones):
    """Fonction qui va donner aleatoirement un possiblité de molecule qui ne contient que des Carbones
    """
    liste_Atomes_Carbones=Molecule()
    liste_Pos_Possibles=[]
    for var1 in range(nbCarbones):
        liste_Atomes_Carbones.add_atome(CARBONE())

    liste_Atomes_Carbones[0].link(liste_Atomes_Carbones[1])
    liste_Pos_Possibles=[1,2,3,5,6,7] #car position 0 et 4 sont prisent pour lier le premier et le second carbone

    n=2
    while n!=len(liste_Atomes_Carbones):
        nbAlea=randrange(n)
        print("nbAlea égal : "+str(nbAlea))
        if liste_Pos_Possibles.count((nbAlea*4)+1) == 1 :

            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]
            print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+1)
            print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)
            n=n+1

        elif liste_Pos_Possibles.count(nbAlea*4+2)==1:

            print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]

            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+2)
            n=n+1
            print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)

        elif liste_Pos_Possibles.count(nbAlea*4+3)==1:

            print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]

            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+3)
            n=n+1
            print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)

        else:
            continue


    return liste_Atomes_Carbones






