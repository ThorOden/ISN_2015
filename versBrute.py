from molecule import *

# definition d'une molecule pour les tests
# atome=[CARBONE(),CARBONE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE()]

# atome[0].link(atome[1])
# atome[0].link(atome[2])
# atome[0].link(atome[3])
# atome[0].link(atome[4])
# atome[1].link(atome[5])
# atome[1].link(atome[6])
# atome[1].link(atome[7])

# moleculeClass=Molecule(atome[0],atome[1],atome[2],atome[3],atome[4],atome[5],atome[6],atome[7])
# moleculeClass=Molecule(atome)


def versFormuleBrute(moleculeClass):
    moleculeComplete = []
    moleculeTypeStr = []
    for i in range(len(moleculeClass)):
        moleculeTypeStr.append(str(moleculeClass[i]))
    for i in range(len(moleculeTypeStr)):
        var1 = moleculeTypeStr[i]
        moleculeComplete.append(var1[0])
    nbC = moleculeComplete.count("C")
    nbH = moleculeComplete.count("H")
    nbO = moleculeComplete.count("O")
    nbN = moleculeComplete.count("N")

    if nbC == 0:
        VnbC = ""
    elif nbC == 1:
        VnbC = "C "
    else:
        VnbC = "C{} ".format(nbC)

    if nbH == 0:
        VnbH = ""
    elif nbH == 1:
        VnbH = "H "
    else:
        VnbH = "H{} ".format(nbH)

    if nbO == 0:
        VnbO = ""
    elif nbO == 1:
        VnbO = "O "
    else:
        VnbO = "O{} ".format(nbO)

    if nbN == 0:
        VnbN = ""
    elif nbN == 1:
        VnbN = "N "
    else:
        VnbN = "N{} ".format(nbN)

    return VnbC + VnbH + VnbO + VnbN
