# Créé par honnoraty, le 26/01/2015 en Python 3.2
from molecule import *

import re

def nomenclature(nomentre):
    #carbone totale / hydrogène totale

    sourcechaine = dict()
    sourcechaine["methan"] = 1,4
    sourcechaine["ethan"] = 2,6
    sourcechaine["propan"] = 3,8
    sourcechaine["butan"] = 4,10
    sourcechaine["pentan"] = 5,12
    sourcechaine["hexan"] = 6,14
    sourcechaine["heptan"] = 7,16
    sourcechaine["octan"] = 8,18
    sourcechaine["nonan"] = 9,20
    sourcechaine["decan"] = 10,22
    sourcechaine["undecan"] = 11,24
    sourcechaine["dodecan"] = 12,26
    sourcechaine["tridecan"] = 13,28

    #carbonne totale / hydrogène totale / nombre de branche / nombre liaison carb===hydro / nombre de liaison carb===carb

    sourcechaine["methyl"] = 1,3,1,3,0,0
    sourcechaine["ethyl"] = 2,5,1,6,1,1
    sourcechaine["dimethyl"] = 2,5,2,3,0,0
    sourcechaine["diethyl"] = 4,9,2,6,1,2
    sourcechaine["trimethyl"] = 3,7,3,3,0,0
    sourcechaine["triethyl"] = 6,13,3,6,1,3

    #carbone / hydrogène / oxygène / liaison / azote
    sourcechaine["ol"] = 0,1,1,1,0,0
    sourcechaine["al"] = 0,0,1,2,0,0
    sourcechaine["one"] = 0,0,1,2,0,0
    sourcechaine["amine"] = 0,2,0,1,1
    sourcechaine["amide"] = 1,2,1,3,1

    chainegenerique = ["methan","ethan","propan","pentan","butan","hexan","octan","nonan","decan","undecan","dodecan","tridecan"]

    branche = ["methyl","ethyl","dimethyl","diethyl","trimethyl","triethyl"]

    fonctionbase = ["ol","al","one","oïque","amine","amide"]

    # nomentre = input("- entre les parties du nom")
    nomentre = nomentre.split("-")

    #print(nomentre)

    nbchainegen = 0
    listbranche = []
    ChAtome = Molecule()#[""]
    positionbranche = []
    positionfonction = 0
    nomMole = ""
    fonction = ""

    nbbranche = 0
    n = 0
    i = 0
    lasti = 0
    z = 0
    y = 0
    positionasign = 1
    position = 0
    hydroSurC = 0
    decahydro = 0
    decacarbo = 0
    decachaine = 0
    nbgroupe = 0
    decabranchecarb = 0
    longlisbr = 0
    longnomin = 0
    decanbrbra = 0
    
    hydro = 0
    carb = 0

    longnomin = len(nomentre)

    for n, elt in enumerate(chainegenerique):
        for i, elt in enumerate(nomentre):
            if nomentre[i] == chainegenerique[n]:
                nbchainegen = n

    for n, elt in enumerate(fonctionbase):
        if (nomentre[longnomin - 1] == fonctionbase[n]):
            fonction = nomentre[longnomin - 1]
            positionfonction = int(nomentre[longnomin - 2])
            hydro -= sourcechaine[fonction][3]



    for n, elt in enumerate(branche):
        for i, elt in enumerate(nomentre):
            if nomentre[i] == branche[n]:
                listbranche.append(branche[n])
                nbbranche += 1
                while nomentre[i-positionasign].isdecimal():
                    positionbranche.append(int(nomentre[i - positionasign]))
                    positionasign += 1
                    position += 1
                positionasign = 1



    (carb,hydro) = sourcechaine[chainegenerique[nbchainegen]]


    for n in range(nbbranche):
        carb, hydro = carb + sourcechaine[listbranche[n]][0] , hydro + sourcechaine[listbranche[n]][1]

    hydro -= nbbranche

    if (fonction != ""):
        hydro -= sourcechaine[fonction][3]


    nomMole = "C" + str(carb) + "H" + str(hydro)
    #print(nomMole)

    #for n in range(position):
        #print(positionbranche[n])

    for n in range(carb):       #Génération des liste d'atome
        ChAtome.add_atome(CARBONE())


    for n in range(hydro):
        ChAtome.add_atome(HYDROGENE())

    carbChaineg = int(sourcechaine[chainegenerique[nbchainegen]][0])
    for n in range(carbChaineg - 1):        #Génération de la chaine principale
        ChAtome[n].link(ChAtome[n + 1])

    #decacarbo = carbChaineg

    #print("décalage:" ,carbChaineg)

    lasti = 0

    for n in range (nbbranche):
        nbgroupe += sourcechaine[listbranche[n]][2]

    for n in range (nbgroupe):
        if(re.search(r"di", listbranche[n])):
            listbranche[n] = listbranche[n][2:]
            listbranche.append(listbranche[n])
        if(re.search(r"tri", listbranche[n])):
            listbranche[n] = listbranche[n][3:]
            listbranche.append(listbranche[n])
            listbranche.append(listbranche[n])

    #print(listbranche)

    for n in range(nbgroupe):       #Ajout des branches
        ChAtome[positionbranche[n] - 1].link(ChAtome[carbChaineg + n + decabranchecarb])
        for i in range(sourcechaine[listbranche[n]][4]):
            ChAtome[carbChaineg + decachaine + decabranchecarb - n + decanbrbra].link(ChAtome[carbChaineg + decachaine + decabranchecarb + 1 - n])
            decabranchecarb += 1

        for i in range(sourcechaine[listbranche[n]][3] - sourcechaine[listbranche[n]][4]): #Création de la chaine avec ajour des carbones
            #print(*ChAtome)
            #print(carb)
            if((i == 2) and (sourcechaine[listbranche[n]][4] == 1)):
                decachaine += 1
            ChAtome[carbChaineg + decachaine].link(ChAtome[carb + decacarbo + decahydro])
            decahydro += 1
        decachaine += 1
        if (nbbranche > 1):
            decanbrbra = 2


    if fonction == "ol":
        ChAtome.add_atome(HYDROGENE())
        ChAtome.add_atome(OXYGENE())
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb + 1])
        ChAtome[hydro + carb + 1].link(ChAtome[hydro + carb])

    if fonction == "al":
        ChAtome.add_atome(OXYGENE())
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb])
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb])


    if fonction == "one":
        ChAtome[hydro + carb] = OXYGENE()
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb])
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb])

    if fonction == "amine":
        ChAtome.add_atome(HYDROGENE())
        ChAtome.add_atome(HYDROGENE())
        ChAtome.add_atome(AZOTE())
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb + 2])
        ChAtome[hydro + carb + 2].link(ChAtome[hydro + carb])
        ChAtome[hydro + carb + 2].link(ChAtome[hydro + carb + 1])

    if fonction == "amide":
        ChAtome.add_atome(HYDROGENE())
        ChAtome.add_atome(HYDROGENE())
        ChAtome.add_atome(AZOTE())
        ChAtome.add_atome(OXYGENE())
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb + 3])
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb + 3])
        ChAtome[positionfonction - 1].link(ChAtome[hydro + carb + 2])
        ChAtome[hydro + carb + 2].link(ChAtome[hydro + carb])
        ChAtome[hydro + carb + 2].link(ChAtome[hydro + carb + 1])


    #2-3-dimethyl-butan-e
    #2-methyl-butan-e
    #2-ethyl-butan-e
    #2-trimethyl-butan-e
    hydroChaineg = int(sourcechaine[chainegenerique[nbchainegen]][1])

    #print("yolo")
    #print(hydroChaineg)
    #print(len(ChAtome))
    #print(carbChaineg)


    for n in range(carbChaineg):
        hydroSurC = 4
        for i in range(len(positionbranche)):
            if(n == (positionbranche[i] - 1)):
                hydroSurC -= 1

        if (n == positionfonction - 1):
                hydroSurC -= sourcechaine[fonction][3]
                #print("ICI ça fait cheeeeeeeeeé")
                #print("sourceef re:",hydroSurC)



        if(((n == 0) or (n == carbChaineg - 1)) and (chainegenerique[nbchainegen] != "methan")):
            hydroSurC -= 1

        elif (chainegenerique[nbchainegen] != "methan"):
            hydroSurC -= 2
            #print("làa aussi")

        #print("Hydro sur Carb")
        #print(hydroSurC)
        #print(*ChAtome)
        #print("valeur de n:",n)

        for y in range(hydroSurC):

            #print("carb",n)
            #print(decacarbo)
            #print("hydro",n + decahydro + carbChaineg + decacarbo + decachaine)
            ChAtome[n].link(ChAtome[n + carb + decacarbo + decahydro])
            #print("liée")
            #print(*ChAtome)
            decahydro += 1
        decahydro -= 1



    #molecule=Molecule(*ChAtome)
    #print(ChAtome)
    #print(type(ChAtome))


    return ChAtome

    ##print(molecule.add_atome)
    ##print(molecule)


    #2-methyl-butan-e
