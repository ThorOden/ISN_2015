# Créé par BOUVIN valentin, le 02/02/2015 en Python 3.2
from molecule import *
from calcul import *
#from versBrute import *

#je te laisse faire la tabutaltion pour la fonction car je n'ai pas un logiel aussi bien que toi qui peux tout faire d'un coup
#le paramètre c'est la variable molecule (on peux l'entrer  comme on veut, ex : c4h10, C4H10, H10 OC, H1C2 ON)
#Par contre ca ne marche pas si tu la rentre sous cette forme : Ch4OO C4H12     avec deux fois des C ou des H


molecule = str(input("entrez votre molécule sous la forme : C6HO4"))
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



if iteration[N]==0 and iteration[O]==0 and iteration[C]!=0 and iteration[H]!=0:
    #on a que des carbones et hydrogènes (alcane ou alcène)
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
elif iteration[N]==0 and iteration[0]!=0 and iteration[C]!=0 and iteration[H]!=0 :
    #on a des carbones, des hydrogènes et des oxygènes (alcool, cétones, acides étanoïque, ester ...)
    if iteration[H]==iteration[C]*2+2:
        #cas le plus simple pas de double liaison
        pass
    elif iteration[C]*2+2<iteration[H] :
        raise ImpossibleCombinaison()
        exit


#ajout des Hydrogenes
MoleculePossible_sansH_.add_atome(HYDROGENE())
for numeroAtome in range(iteration[C]+iteration[N]+iteration[O]):
    try :
        for n in range(4):
            print("avant ereur : ",len(MoleculePossible_sansH_))
            MoleculePossible_sansH_[numeroAtome].link(MoleculePossible_sansH_[-1])
            MoleculePossible_sansH_.add_atome(HYDROGENE())

    except OverLinked:

        print("numero de l'atome : ",numeroAtome+1)
        print("il y a ",n,"Hydorgene rajoute")

del MoleculePossible_sansH_[-1]
MoleculePossiblecomplete=MoleculePossible_sansH_

#return MoleculePossiblecomplete

#formuleBrute=versFormuleBrute(MoleculePossiblecomplete)
#print(formuleBrute)



