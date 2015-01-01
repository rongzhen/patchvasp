#! /usr/bin/python3.2

import os
import shutil


fileINCAR='/home/rongzhen/workplace/python_coding/final/FIELS/INCAR'
fileKPOINTS="/home/rongzhen/workplace/python_coding/final/FIELS/KPOINTS"
filePOSCAR="/home/rongzhen/workplace/python_coding/final/FIELS/POSCAR"
filePOTCAR="/home/rongzhen/workplace/python_coding/final/FIELS/POTCAR/PBE"
fileRUNSCRIPT="/home/rongzhen/workplace/python_coding/final/FIELS/RUNSCRIPT"


#A=['Cu'];
#B=['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu', 'Zn'];
#C=['Ti', 'Si', 'Ge','Sn'];
#D=['S', 'Se'];

A=['Cu'];
B=['Sc','Ti','Cu', 'Zn'];
C=['Ti', 'Si'];
D=['S', 'Se'];

phaseN=['FM','AFM1','AFM2']
structureN=['KS', 'ST']


#def genPOSCAR(eleA, eleB, eleC, eleD):



#def genINCAR(eleA, eleB, eleC, eleD):



#################### Function: generate all the KPOINTS###################
def genKPOINTS():
   filek=fileKPOINTS+"/*"
   os.system("cp %s ." % filek) 



#################### Function: generate all the POTCAR###################
def genPOTCAR(eleA, eleB, eleC, eleD):

    pathstrA=(filePOTCAR+"/"+eleA+"/POTCAR")
    pathstrB=(filePOTCAR+"/"+eleB+"/POTCAR")
    if eleC == "Ge" or eleC == "Sn":
        pathstrC=(filePOTCAR+"/"+eleC+"_d/POTCAR")
    else:
        pathstrC=(filePOTCAR+"/"+eleC+"/POTCAR")
    pathstrD=(filePOTCAR+"/"+eleD+"/POTCAR")

    fin1 = open(pathstrA, "r")
    data1 = fin1.read()
    fin1.close()

    fin2 = open(pathstrB, "r")
    data2 = fin2.read()
    fin2.close()

    fin3 = open(pathstrC, "r")
    data3 = fin3.read()
    fin3.close()

    fin4 = open(pathstrD, "r")
    data4 = fin4.read()
    fin4.close()

    if eleA == eleB:
        combined_data = data1 + data3 + data4
	# if B==C==Ti
    elif eleB == eleC:
        combined_data = data1 + data2 + data4
	# normal case 
    else:
        combined_data = data1 + data2 + data3 + data4
	
    fout = open("POTCAR", "w")
    fout.write(combined_data)
     


#################### Function: generate all the runscript.sh###################
def genRUN():
    filerun=fileRUNSCRIPT+"/*"
    os.system("cp %s ." % filerun)


#################### Function: generate all the directories ###################
def genDir(eleA, eleB, eleC, eleD):

#    prevDir = os.getcwd();

    if eleA == eleB:
        name = eleA+str(6)+eleC+str(2)+eleD+str(8)
        labelName = "AeB"
    elif eleB == eleC:
        name = eleA+str(4)+eleB+str(4)+eleD+str(8)
        labelName = "Bec"
    else:
        name = eleA+str(4)+eleB+str(2)+eleC+str(2)+eleD+str(8)
        labelName = "ABCD"

    os.mkdir(name)
    os.chdir(name)
    
    for structure in structureN:
        os.mkdir(structure)
        os.chdir(structure)
        for phase in phaseN: 
            os.mkdir(phase)

        os.chdir(os.pardir)

    return (name, labelName)

#################### main program ###################
for eleA in A:
   for eleB in B:
        for eleC in C:
            for eleD in D:

                prevDir = os.getcwd()

                dirName, labelName=genDir(eleA, eleB, eleC, eleD)
                
                os.chdir(prevDir)
                os.chdir(dirName)

                for structure in structureN:
                    os.chdir(structure)

                    for phase in phaseN:
                        os.chdir(phase)

                        genKPOINTS()
                        genRUN()
                        genPOTCAR(eleA, eleB, eleC, eleD)

                        os.chdir(os.pardir)
                    os.chdir(os.pardir)
                os.chdir(prevDir)
                     
