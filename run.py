#! /usr/bin/python3.2

import os
import shutil
import re


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
B=['Sc','Cu','Ti'];
C=['Ti','Si'];
D=['S'];

phaseN=['FM','AFM1','AFM2','AFM3']
structureN=['KS', 'ST']
incarN=['INCAR.pbe.relax1','INCAR.pbe.relax2','INCAR.pbe.relax3','INCAR.pbe.relax4','INCAR.pbe.relax5']
 
#################### Function: replace many words###################
def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

#################### Function: generate all the POSCAR###################
def genPOSCAR(eleA, eleB, eleC, eleD, structure, phase):

    fileP=filePOSCAR+"/"+structure+"/"+phase
    os.system("cp %s ." % fileP) 

	# if A==B==Cu
    if eleA == eleB:
        strElementName= "      "+eleA+"   "+eleC+"   "+eleD
        strElementNumber="    "+str(6)+"   "+str(2)+"   "+str(8)
	# if B==C==Ti
    elif eleB == eleC:
        strElementName= "      "+eleA+"   "+eleB+"   "+eleD
        strElementNumber="    "+str(4)+"   "+str(4)+"   "+str(8)
	# normal case 
    else:
        strElementName= "      "+eleA+"   "+eleB+"   "+eleC+"   "+eleD
        strElementNumber="    "+str(4)+"   "+str(2)+"   "+str(2)+"   "+str(8)
    
    fin = open(phase, "r")
    strFin=fin.read() 
    fin.close()
    
    word_dic = {
    'elementsname': strElementName,
    'elementsnumber': strElementNumber}

    strFout=replace_words(strFin, word_dic)

    fout = open("POSCAR", "w")
    fout.write(strFout)
    fout.close()

    os.system("rm %s" % phase) 



#################### Function: generate all the INCAR###################
def genINCAR(eleA, eleB, eleC, eleD, phase):

    dictU={'Sc': 4.4,
           'Ti': 4.4,
           'V' : 2.7,
           'Cr': 3.5,
           'Mn': 4.0,
           'Fe': 4.6,
           'Co': 5.0,
           'Ni': 5.1,
           'Cu': 4.0,
           'Zn': 7.5}

    fileI=fileINCAR+"/*"
    os.system("cp %s ." % fileI)

	# if A==B==Cu
    if eleA == eleB:
        strLdauJ= "LDAUJ      =   0.0   0.0    0.0"

        if eleC == "Ti":
            strLdauL= "LDAUL      =   2     2      0"
            strLdauU= "LDAUU      =   4.0   4.4    0.0" 
            if phase == 'FM':
                strMagmom="6*0.0 4.0 4.0 8*0.0"
            else:
                strMagmom="6*0.0 4.0 -4.0 8*0.0"
        else:
            strLdauL= "LDAUL      =   2     0      0"
            strLdauU= "LDAUU      =   4.0   0.0    0.0"
            strMagmom="6*0.0 2*0.0 8*0.0"
	# if B==C==Ti
    elif eleB == eleC:
        strLdauJ= "LDAUJ      =   0.0   0.0    0.0"
        strLdauL= "LDAUL      =   2     2      0"
        strLdauU= "LDAUU      =   4.0   4.4    0.0"
        if phase == 'FM':
            strMagmom="4*0.0 4*4.0 8*0.0"
        else:
            strMagmom="4*0.0 4.0 -4.0 4.0 -4.0 8*0.0"
	# normal case 
    else:
        strLdauJ= "LDAUJ      =   0.0   0.0    0.0   0.0"

        if eleC == "Ti":
            strLdauL= "LDAUL      =   2     2      2     0"
            strLdauU= "LDAUU      =   4.0   "+str(dictU[eleB])+"    "+str(dictU[eleC])+"   0.0"
            if phase == 'FM':
                strMagmom="4*0.0 4*4.0 8*0.0"
            else:
                strMagmom="4*0.0 4.0 -4.0 4.0 -4.0 8*0.0"
        else:
            strLdauL= "LDAUL      =   2     2      0     0"
            strLdauU= "LDAUU      =   4.0   "+str(dictU[eleB])+"    0.0   0.0"
            if phase == 'FM':
                strMagmom="4*0.0 2*4.0 2*0.0 8*0.0"
            else:
                strMagmom="4*0.0 4.0 -4.0 2*0.0 8*0.0"

    nList = len(incarN)
    for i in range(0, nList-1):

        incarF=fileINCAR+"/"+incarN[i]

        fin = open(incarF, "r")
        strFin=fin.read() 
        fin.close()

        os.system("rm %s" % incarF)

        word_dic = {
        'MAGMOMline': strMagmom,
        'LDAUJline' : strLdauJ,
        'LDAULline' : strLdauL,
        'LDAUUline' : strLdauU}

        strFout=replace_words(strFin, word_dic)

        fout = open(incarF, "w")
        fout.write(strFout)
        fout.close()

#################### Function: generate all the KPOINTS###################
def genKPOINTS():
   fileK=fileKPOINTS+"/*"
   os.system("cp %s ." % fileK) 



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
                print "compound name: ", dirName                
                os.chdir(prevDir)
                os.chdir(dirName)

                for structure in structureN:
                    os.chdir(structure)

                    for phase in phaseN:
                        os.chdir(phase)

                        genKPOINTS()
                        genRUN()
                        genPOTCAR(eleA, eleB, eleC, eleD)
                        genPOSCAR(eleA, eleB, eleC, eleD, structure, phase)
                        genINCAR(eleA, eleB, eleC, eleD, phase)

                        os.chdir(os.pardir)
                    os.chdir(os.pardir)
                os.chdir(prevDir)
                     
