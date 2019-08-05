import sys
import os
import numpy

#The U(0K) of elements from atomref.txt ; Unit: Hartree
U_H = -0.500273
U_C = -37.846772
U_N = -54.583861
U_O = -75.064579
U_F = -99.718730

U = [U_H, U_C, U_N, U_O, U_F]

#The enthalpies of formation of elements ar 0K (delta Hf(0K)) from Thermochemistry in Gaussian ; Unit: kcal/mol
Hf_H = 51.63
Hf_C = 169.98
Hf_N = 112.53
Hf_O = 58.99
Hf_F = 18.47

Hf = [Hf_H, Hf_C, Hf_N, Hf_O, Hf_F]

#The enthalpies of corrections of the atomic elements (H◦X(298K) − H◦X(0K)) from Thermochemistry in Gaussian ; Unit: kcal/mol
Hc_H = 1.01
Hc_C = 0.25
Hc_N = 1.04
Hc_O = 1.04
Hc_F = 1.05

Hc = [Hc_H, Hc_C, Hc_N, Hc_O, Hc_F]

#For exercise1 question 6 Show Molecular Formula as SMILES and the heat of the formation with the following format
#SMILES_1  Hf_1
#SMILES_2  Hf_2



def calculate(chem):
    parsed = list(chem)

    # Split chem string into [Atom, Number...] pattern
    # Atoms are str, Numbers are int
    temp = []
    for v in parsed:
        if not v.isdigit():
            if len(temp) == 0:
                temp.append(v)
            elif type(temp[-1]) == int:
                temp.append(v)
            elif v.islower():
                temp[-1] = f'{temp[-1]}{v}'
            else:
                temp.append(v)
        else:
            if type(temp[-1]) == int:
                temp[-1] = temp[-1] * 10 + int(v)
            else:
                temp.append(int(v))

    parsed = temp
    temp = []

    # Insert omitted Atom Number
    for v in parsed:
        if type(v) == str and len(temp) > 0 and type(temp[-1]) == str:
            temp.append(1)
        temp.append(v)

    # Insert missed number for last atom
    if type(temp[-1]) == str:
        temp.append(1)

    parsed = temp
    result = {}

    # Reduce result into a dict
    for i, v in enumerate(parsed):
        if type(v) == str:
            if not v in result.keys():
                result[v] = 0
        else:
            result[parsed[i - 1]] += v

    return result

#Define MultipleList 

def MultipleList(list1,list2):
    func = lambda a,b: a*b
    List_result = list(map(func, list1, list2))
    summation = 0
    for element in List_result:
        summation += element
    return summation


#Define The heat of the formation

def Heat_of_formation():
    Heat_of_formation_0K = MultipleList(list_ShowAtoms,Hf)-627.5095*(MultipleList(list_ShowAtoms,U)-float(U_Molecule_0K))     #Hf(0K)=Enthalpies of formation of elements - Atomization energy of the molecule
    Enthalpy_Correction_of_Molecule = float(H_Molecule_298K)-float(U_Molecule_0K)    #Hcorr=H(298K,Molecules)-U(0K,Molecules)
    Enthalpy_Correction_of_Atom = MultipleList(list_ShowAtoms,Hc)
    Heat_of_formation_298K = Heat_of_formation_0K + 627.5095*Enthalpy_Correction_of_Molecule - Enthalpy_Correction_of_Atom
    return Heat_of_formation_298K


#Read file
path = r"C:\\Users\\ms860\\Desktop\\Exercise1\\dsgdb9nsd.xyz"
data = os.listdir(path)
f1 = open('Heat_Formation_of_134K_Molecules.txt', 'w')
for filename in data:
    filename_path=r"C:\\Users\\ms860\\Desktop\\Exercise1\\dsgdb9nsd.xyz\\" + filename
    f2 = open(filename_path,'r')
    line = f2.readlines()
    #U_Molecule_298K = d1.replace(' ','\t').split('\t')[13]     #Internal Energy at 298.15K
    U_Molecule_0K = line[1].replace(' ','\t').split('\t')[12]   #Internal Energy at 0K = Enthalpy at 0K
    H_Molecule_298K = line[1].replace(' ','\t').split('\t')[14]   #Enthapy at 298.15K
    SMILES = line[-2].replace(' ','\t').split('\t')[0]   #SMILES
    InChI =  line[-1].split('/')[1]   #InChI
    f2.close()
    list_ShowAtoms = []
    counts_dict = calculate(InChI)
    atoms = ["H", "C", "N", "O", "F"]
    list_ShowAtoms = [(counts_dict[a] if a in counts_dict.keys() else 0) for a in atoms]
    f1.write('{} {:.4f}\n'.format(SMILES, Heat_of_formation()))
    #f1.write('%-70s%.2f\n' % (SMILE, Heat_of_formation()))
f1.close()
