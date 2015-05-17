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
        #print("nbAlea égal : "+str(nbAlea))
        if liste_Pos_Possibles.count((nbAlea*4)+1) == 1 :

            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]
            #print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            #print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+1)
            #print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)
            n=n+1

        elif liste_Pos_Possibles.count(nbAlea*4+2)==1:

            #print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]

            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            #print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+2)
            n=n+1
            #print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)

        elif liste_Pos_Possibles.count(nbAlea*4+3)==1:

            #print("liste_Pos_Possibles avant incrémentation : ",liste_Pos_Possibles)
            liste_Atomes_Carbones[n].link(liste_Atomes_Carbones[nbAlea])
            dernierDeLaListe=liste_Pos_Possibles[-1]

            for var1 in range(3):
                liste_Pos_Possibles.append(dernierDeLaListe+(var1+2))
            #print("liste_Pos_Possibles après incrémentation : ",liste_Pos_Possibles)
            liste_Pos_Possibles.remove(nbAlea*4+3)
            n=n+1
            #print("liste_Pos_Possibles après supression : ",liste_Pos_Possibles)

        else:
            continue


    return liste_Atomes_Carbones


def UneChaineOxygenee(nbCarbones,nbOxygene):
    liste_Atomes_Class=Molecule()
    liste_Atomes_NonLink=[]
    liste_Atomes_Dispo=[]
    for var1 in range(nbCarbones):
        liste_Atomes_Class.add_atome(CARBONE())
        liste_Atomes_NonLink.append("c")
    for var1 in range(nbOxygene):
        liste_Atomes_Class.add_atome(OXYGENE())
        liste_Atomes_NonLink.append("o")

    liste_Atomes_Dispo.append(0)#ce sera tjr le carbonne zero qui sera dispo
    liste_Atomes_NonLink[0]=0#car dans tout les cas c'est un carbonne et il sera toujours lie

    nombre_d_Atome_Liee=1
    while nombre_d_Atome_Liee!=len(liste_Atomes_Class):
        nbAlea1=randrange(len(liste_Atomes_NonLink)) #pour choisir lequel des atomes non lie va etre pris

        if liste_Atomes_NonLink[nbAlea1]==0:#le 0 qui peut etre dans la liste_Atome_NonLink veux dire que l'atome a deja ete choisi on fait cela pour choisir au hasard un carbone ou un oxygene
            #print("nbAlea1 etait egal a : ",nbAlea1)
            continue

        else:
            stop=0
            while stop!=1:

                #print("nbAlea1 est finalement egal a : ",nbAlea1)

                nbAlea2=randrange(nombre_d_Atome_Liee)#pour choisir lequel des atome déja assemble va recevoir le nouvel atome
                #print("nbAlea2 egal : ",nbAlea2)

                try:
                    liste_Atomes_Class[nbAlea1].link(liste_Atomes_Class[liste_Atomes_Dispo[nbAlea2]])
                    stop=1
                except OverLinked:
                    liste_Atomes_Class[nbAlea1].delink()
                    #print("surlie")
                    #cela veux dire que l'atome auquel on veux se lier est deja trop lie, avant on avait pas besoin de faire ca car il n'y avait qu des carbones
                    continue
            liste_Atomes_NonLink[nbAlea1]=0
            liste_Atomes_Dispo.append(nbAlea1)

        nombre_d_Atome_Liee+=1
        #print("on incremente ",nombre_d_Atome_Liee)

    liste_Atomes_liee=liste_Atomes_Class
    return liste_Atomes_liee








