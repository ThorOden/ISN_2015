# Nomenclature
# Copyright (C) 2015 BOUVIN Valentin, HONNORATY Vincent, LEVY-FALK Hugo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Créé par honnoraty, le 26/01/2015 en Python 3.2
from molecule import *
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

sourcechaine["methyl"] = 1,3
sourcechaine["ethyl"] = 2,5
sourcechaine["dimethyl"] = 2,5
sourcechaine["diethyl"] = 4,9
sourcechaine["trimethyl"] = 3,7
sourcechaine["triethyl"] = 6,12

chainegenerique = ["methan","ethan","propan","butan","hexan","octan","nonan","decan","undecan","dodecan","tridecan"]

branche = ["methyl","ethyl","dimethyl","diethyl","trimethyl","triethyl"]

nomentre = input("- entre les parties du nom")
nomentre = nomentre.split("-")

print(nomentre)

nbchainegen = 0
listbranche = [""]
ChAtome = [""]
positionbranche = [""]
nomMole = ""

for n, elt in enumerate(chainegenerique):
    for i, elt in enumerate(nomentre):
        if nomentre[i] == chainegenerique[n]:
            nbchainegen = n

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


for n, elt in enumerate(branche):
    for i, elt in enumerate(nomentre):
        if nomentre[i] == branche[n]:
            listbranche[nbbranche] = branche[n]
            nbbranche += 1
            listbranche.append(1)
            while nomentre[i-positionasign].isdecimal():
                positionbranche[position] = int(nomentre[i - positionasign])
                positionbranche.append(1)
                positionasign += 1
                position += 1
            positionasign = 0



(carb,hydro) = sourcechaine[chainegenerique[nbchainegen]]
for n in range(nbbranche):
    carb, hydro = carb + sourcechaine[listbranche[n]][0], hydro + sourcechaine[listbranche[n]][1] - nbbranche

nomMole = "C" + str(carb) + "H" + str(hydro)
print(nomMole)

for n in range(position):
    print(positionbranche[n])

for n in range(carb):       #Génération des liste d'atome
    ChAtome.append(1)
    ChAtome[n] = CARBONE()


for n in range(hydro):
    ChAtome.append(1)
    ChAtome[n + carb] = HYDROGENE()


carbChaineg = int(sourcechaine[chainegenerique[nbchainegen]][0])
for n in range(carbChaineg - 1):        #Génération de la chaine principale
    ChAtome[n].link(ChAtome[n + 1])

#decacarbo = carbChaineg

print("décalage:" ,carbChaineg)

lasti = 0

for n in range(nbbranche):       #Ajout des branches
    ChAtome[positionbranche[n] - 1].link(ChAtome[carbChaineg + n])
    for i in range(sourcechaine[listbranche[n]][1] + sourcechaine[listbranche[n]][0] - 1):
        print("Posi hydro: ",carbChaineg + decachaine + decacarbo)
        print("chaine",*ChAtome)
        decacarbo += 1
        ChAtome[carbChaineg + n + decachaine].link(ChAtome[carbChaineg + decachaine + decacarbo])
        print(sourcechaine[listbranche[n]][1] + sourcechaine[listbranche[n]][0])

        if ((lasti + 2 == i) and (decachaine == 0 ) or (lasti + 3 == i)):
            decachaine += 1
            lasti = i
        if(i == 2):
            decacarbo -= 1
        if(i == 5 and (listbranche[n] == "trimethyl")):
            decacarbo -= 1








#2-methyl-butan-e
#2-ethyl-butan-e
#2-trimethyl-butan
hydroChaineg = int(sourcechaine[chainegenerique[nbchainegen]][1])

print("yolo")
print(hydroChaineg)
print(len(ChAtome))
print(carbChaineg)

for n in range(carbChaineg):
    hydroSurC = 4
    for z in range(position):

        try:
            if(n == positionbranche[n]):
                hydroSurC -= 1
        except IndexError:
            pass

    if(((n == 0) or (n == carbChaineg - 1)) and (chainegenerique[nbchainegen] != "methan")):
        hydroSurC -= 1
    elif (chainegenerique[nbchainegen] != "methan"):
        hydroSurC -= 2

    print("Hydro sur Carb")
    print(hydroSurC)
    print(*ChAtome)
    print("valeur de:",n)

    for y in range(hydroSurC):
        print("crab",n)
        print(decacarbo)
        print("hydro",decahydro + carbChaineg + decacarbo + decachaine)
        ChAtome[n].link(ChAtome[n + decahydro + carbChaineg + decacarbo + decachaine])
        print("liée")
        print(*ChAtome)
        decahydro += 1
    decahydro -= 1



#molecule=Molecule(*ChAtome)


print(*ChAtome)

#print(molecule.add_atome)
#print(molecule)


#2-methyl-butan-e
