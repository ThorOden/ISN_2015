# Créé par BOUVIN valentin, le 02/02/2015 en Python 3.2
from molecule import *
from calcul import *
#from versBrute import *

#le paramètre c'est la variable molecule (on peux l'entrer  comme on veut, ex : c4h10, C4H10, H10 OC, H1C2 ON)
#Par contre ca ne marche pas si tu la rentre sous cette forme : Ch4OO C4H12     avec deux fois des C ou des H

class ImpossibleCombinaison(Exception):
    pass
class HydrogeneProblem(Exception):
    pass

def bruteVersClass(molecule):
    """Fonction qui passe de la formule brute (C4 H14 O2) vers la forme "numérisée" de la la classe Molecule
    une chaine de  caractère est demandée
    """
    # molecule = str(input("entrez votre molécule sous la forme : C6HO4"))
    if molecule[-1].isalpha()==True:
        molecule=molecule +"1"
    else:
        pass
    #convertion de l'entrée en deux listes : atome et itération
    i=0
    atome=[]
    iteration=[]
    while i!=len(molecule):
        if (i+2!=len(molecule)) and molecule[i].isalpha()==True and molecule[i+1].isnumeric()==True and molecule[i+2].isnumeric()==True:
            atome.append(molecule[i].upper())
            iteration.append(int(molecule[i+1])*10+int(molecule[i+2]))
            i+=3
        elif (i+1!=len(molecule)) and molecule[i].isalpha()==True and molecule[i+1].isnumeric()==True:
            atome.append(molecule[i].upper())
            iteration.append(int(molecule[i+1]))
            i+=2

        else:
            atome.append(molecule[i].upper())
            iteration.append(1)
            i+=1
    iteration.append(0) #c'est pour pouvoir gérer les atomes abscent

    #définition de tout les atomes présents :
    liste_Carbones=[]
    liste_Hydrogenes=[]
    liste_Azote=[]
    liste_Oxygene=[]
    #les variables C,H,O,N sont en fait le rang des atomes dans la variable atome
    try:
        C=atome.index("C")
    except ValueError:
        C=-1 #rang du "0" dans itération
    try:
        H=atome.index("H")
    except ValueError:
        H=-1
    try:
        O=atome.index("O")
    except ValueError:
        O=-1
    try:
        N=atome.index("N")
    except ValueError:
        N=-1

    print(molecule)
    print("Nombre de carbones ={}".format(iteration[C]))
    print("Nombre de Hydrogène ={}".format(iteration[H]))
    print("Nombre de d'Azotes ={}".format(iteration[N]))
    print("Nombre de d'Oxygène ={}".format(iteration[O]))


    #début de la recherche des possiblitées

    MoleculePossible_sansH_= Molecule()

    if iteration[H]%2==1:
        raise ImpossibleCombinaison()
        exit

    elif iteration[C]==1 and iteration[H]==4:
        #traitement du cas particulier de CH4
        MoleculePossible_sansH_.add_atome(CARBONE())
        MoleculePossible_sansH_.add_atome(HYDROGENE())
        for n in range(3):
                MoleculePossible_sansH_[0].link(MoleculePossible_sansH_[-1])
                MoleculePossible_sansH_.add_atome(HYDROGENE())
        return MoleculePossible_sansH_

    elif iteration[N]==0 and iteration[O]==0 and iteration[C]!=0 and iteration[H]!=0:
        #on a que des carbones et hydrogènes (alcane ou alcène)
        print ("cas avec que carbones")
        if iteration[C]*2+2==iteration[H] :
            #cas le plus simple pas de double liaison
            print("cas simple")
            MoleculePossible_sansH_= UneChaineCarbonnee(iteration[C])
        elif iteration[C]*2+2<iteration[H] :
            raise ImpossibleCombinaison()
            exit
        else:
            print("cas avec des doubles liasons")
            Nombre_de_double_Liaisons=(iteration[C]*2+2)-iteration[H]
            pass

    elif iteration[N]==0 and iteration[O]!=0 and iteration[C]!=0 and iteration[H]!=0 :
        print("cas avec oxygene")
        #on a des carbones, des hydrogènes et des oxygènes (alcool, cétones, acides étanoïque, ester ...)
        if iteration[H]==iteration[C]*2+2:
            #cas le plus simple pas de double liaison
            print("cas simple")
            MoleculePossible_sansH_=UneChaineOxygenee(iteration[C],iteration[O])
        elif iteration[C]*2+2<iteration[H] :
            raise ImpossibleCombinaison()
            exit
        else:
            print("cas avec des doubles liasons")
            Nombre_de_double_Liaisons=(iteration[C]*2+2)-iteration[H]
            pass


    #ajout des Hydrogenes
    nbHydrogene_cree=0
    MoleculePossible_sansH_.add_atome(HYDROGENE())
    for numeroAtome in range(iteration[C]+iteration[N]+iteration[O]):
        try :
            for n in range(4):
                #print("avant ereur : ",len(MoleculePossible_sansH_))
                MoleculePossible_sansH_[numeroAtome].link(MoleculePossible_sansH_[-1])
                MoleculePossible_sansH_.add_atome(HYDROGENE())
                nbHydrogene_cree+=1
        except OverLinked:

            #print("numero de l'atome : ",numeroAtome+1)
            #print("il y a ",n,"Hydorgene rajoute")
            pass

    del MoleculePossible_sansH_[-1]
    MoleculePossiblecomplete=MoleculePossible_sansH_

    if iteration[H]!=nbHydrogene_cree:
        raise HydrogeneProblem()

    return MoleculePossiblecomplete

    #formuleBrute=versFormuleBrute(MoleculePossiblecomplete)
    #print(formuleBrute)

#print(versFormuleBrute(bruteVersClass("c4o3h10")))

