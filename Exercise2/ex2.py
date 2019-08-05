from rdkit import Chem
from rdkit.Chem import AllChem
import sys
import random

import matplotlib
import matplotlib.pyplot as plt  # plot loss and feature map

from keras.layers import Input, Dense, Activation
from keras.models import Sequential
from keras import callbacks
from keras import optimizers
from keras import regularizers

import numpy as np

#open & read file
f1 = open ('/Users/terryli/Desktop/Lab/Exercise1/SMILES_and_heat_of_formation_for_134K_molecules.txt', 'r')
lines = f1.readlines()
# index number in test
test_indexs = random.sample(range(133885), int(133885/10))  # ramdomly fetch int element from list
test_dataset = [lines[i] for i in test_indexs]
train_dataset = list(set(lines) - set(test_dataset))
#train_dataset = list(set(list(range(133885))) - set(test_indexs))
f1.close()

    
"""
A = [1,2,3,4,5]
B = [4,5,6,7]
C = list(set(A)-set(B))
print(C) = [1,2,3]
"""

train_smiles = [line.split()[0] for line in train_dataset]  #smiles for training set
train_heat = [float(line.split()[1]) for line in train_dataset]  #heat of formation smiles for training set
test_smiles = [line.split()[0] for line in test_dataset]  #smiles for  testset
test_heat = [float(line.split()[1]) for line in test_dataset]  #heat of formation smiles for testset


#convert SMILES to ECFP fingerprint
train_mols = [Chem.MolFromSmiles(s) for s in train_smiles]
train_ecfp = [AllChem.GetMorganFingerprintAsBitVect(
            mol, radius=2, nBits=512, useChirality=False, useBondTypes=False, useFeatures=False) for mol in train_mols]
test_mols = [Chem.MolFromSmiles(s) for s in test_smiles]
test_ecfp = [AllChem.GetMorganFingerprintAsBitVect(
            mol, radius=2, nBits=512, useChirality=False, useBondTypes=False, useFeatures=False) for mol in test_mols]


"""
f2 = open ('D:\Exercise2\Heat_Formation_of_134K_Molecules.txt', 'r')
for line2 in open ('D:\Exercise2\Heat_Formation_of_134K_Molecules.txt', 'r') :
    str2 = f2.readline()
f2.close()

train_heat = [float(str2.split(',')) for str in train_indexs]
test_heat = [float(str2.split(',')) for str in test_indexs]

#append number into test set
test_ecfp = []
for i in test_indexs :
    test_ecfp.append(total_fp[i])
test_heat = []
for i in test_indexs :
    test_heat.append(heat_list[i])

train_ecfp = []
for i in train_indexs :
    train_ecfp.append(total_fp[i])
train_heat = []
for i in train_indexs :
    train_heat.append(heat_list[i])
"""

x_train = np.array(train_ecfp)
y_train = np.array(train_heat).reshape((120497,1))   #133885-13388=120497
x_test = np.array(test_ecfp)
y_test = np.array(test_heat).reshape((13388,1))



#Build Neural Network
model = Sequential()
model.add(Dense(50, activation = 'tanh', input_dim = x_train.shape[1], name = 'dense1', kernel_regularizer=regularizers.l2(0.0001)))
model.add(Dense(1, activation = None, name = 'dense2'))
lr = 0.0001
epoch = 500
sgd = optimizers.SGD(lr=lr, decay=1e-8, momentum=0.05, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics = ['accuracy'])        

early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0.05, mode ='auto', patience=15, baseline=None, restore_best_weights=False)
hist = model.fit(x_train, y_train, batch_size = 256, epochs = epoch, validation_split = 0.2, callbacks = [early_stopping])
loss, acc = model.evaluate(x_test, y_test, batch_size=256)
print('Testset loss : %.4f' % (loss)) 

###Predict Furfuryl alcohol
predict_smiles = 'C1=COC(=C1)CO'
predict_mol = Chem.MolFromSmiles(predict_smiles)
predict_fp = AllChem.GetMorganFingerprintAsBitVect(
        predict_mol, radius=2, nBits=512, useChirality=False, useBondTypes=False, useFeatures=False)    
furfuryl_alcohol_fp = np.array(predict_fp).reshape((1,512))
furfuryl_alcohol_Hf = model.predict(furfuryl_alcohol_fp)
print('The heat of formation of Furfuryl alcohol is predicted as %.4f kcal/mol' % (furfuryl_alcohol_Hf[0,0]))  
print('The heat of formation from NIST is -50.67 kcal/mol') 
