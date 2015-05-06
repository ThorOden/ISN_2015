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

from molecule import *

# #definition d'une molecule pour les tests
# atome=[CARBONE(),CARBONE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE(),HYDROGENE()]

# atome[0].link(atome[1])
# atome[0].link(atome[2])
# atome[0].link(atome[3])
# atome[0].link(atome[4])
# atome[1].link(atome[5])
# atome[1].link(atome[6])
# atome[1].link(atome[7])

# moleculeClass=Molecule(atome[0],atome[1],atome[2],atome[3],atome[4],atome[5],atome[6],atome[7])
# #moleculeClass=Molecule(atome)

def versFormuleBrute(moleculeClass) :
    moleculeComplete=[]
    moleculeTypeStr=[]
    for i in range(len(moleculeClass)):
        moleculeTypeStr.append(str(moleculeClass[i]))
    for i in range(len(moleculeTypeStr)):
        var1=moleculeTypeStr[i]
        moleculeComplete.append(var1[0])
    nbC=moleculeComplete.count("C")
    nbH=moleculeComplete.count("H")
    nbO=moleculeComplete.count("O")
    nbN=moleculeComplete.count("N")
    
    if nbC==0:
        VnbC=""
    elif nbC==1:
        VnbC="C "
    else:
        VnbC="C{} ".format(nbC)
    
    
    if nbH==0:
        VnbH=""
    elif nbH==1:
        VnbH="H "
    else:
        VnbH="H{} ".format(nbH)
    
    if nbO==0:
        VnbO=""
    elif nbo==1:
        VnbO="O "
    else:
        VnbO="O{} ".format(nbO)
    
    if nbN==0:
        VnbN=""
    elif nbN==1:
        VnbN="N "
    else:
        VnbN="N{} ".format(nbN)
    
    return VnbC+VnbH+VnbO+VnbN
    