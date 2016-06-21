# -*- coding: utf-8 -*-
# Vincent Popie

# Ce programme calcule la transformée de Fourier
# des débits à l'interieur de la perforation

import numpy as np
import scipy.fftpack as fft
import matplotlib.pyplot as plt


# A enregistrer dans un fichier
x = np.array([-0.0016, -0.0014, -0.0012, -0.00102, -0.001, -0.00098, 
	          -0.0009, -0.0008, -0.0007, -0.0006, -0.0005, -0.0004, 
	          -0.0003, -0.0002, -0.0001, -0.00002, 0.000, 0.00002, 
	           0.0002, 0.0004, 0.0006])

nb_coupes = len(x)

f=open('../DATA/position_coupes.dat','w')
for i in range (0,nb_coupes):
		f.write('{:1.7e} {:1.7e}\n' .format(x[i], 0))


#########################
## Lecture des données ##
#########################

data = np.loadtxt('../DATA/temporel/debit_perfo.dat')
nb_capteurs = data.shape[1]-1
print('Nombre de capteurs :', nb_capteurs)

t = data[:,0]
debit = data[:,1:nb_coupes + 1]

####################
## Parametre simu ##
####################

r = 0.0005
R = 0.003
aire = np.pi*r*r
aire_guide = np.pi*R*R
rho = 1.204
c = 340
v_z_moy = debit/aire_guide*rho*c
debit = v_z_moy


###########################
## Préparation de la FFT ##
###########################

dt = t[1]-t[0]

idebut = 19
ifin = -1
print 
print
print("ATTENTION CEST LES VITESSES GUIDES")
print
print("Temps de debut pour Fourier :", t[idebut])
print("Iteration de fin", t[ifin])

t_fourier = t[idebut:ifin]
debit_fourier = debit[idebut:ifin]
debit_mean =  np.mean(debit_fourier,axis=0)

for i in range(0,nb_coupes):
	debit_fourier[:,i] = debit_fourier[:,i]

######################
## Calcul de la FFT ##
######################

N=len(t_fourier)
f=fft.fftfreq(N,dt)
print('Verification de la gamme de frequence')
print(f[0:10])

debit_freq=np.empty([N,nb_coupes],dtype='complex')
for i in range(0,nb_coupes):
	debit_freq[:,i]=fft.fft(debit_fourier[:,i])

##########################################
# Tracé des courbes pour vérifier la FFT #
##########################################

plt.figure(10)
plt.subplot(2,1,1)

plt.plot(f, np.real(debit_freq[:,5]),'o')
plt.subplot(2,1,2)

plt.plot(f, np.imag(debit_freq[:,5]),'o')
plt.show()

#plt.savefig('fourier.eps', format='eps')
#plt.savefig('fourier.pdf', format='pdf')


# Multiplication par le bon facteur
debit_freq_fin = 2.0/N * debit_freq[4,:]

print('Transformee de Fourier terminee')


#########################
# Ecriture des fichiers #
#########################

real_var = np.empty([nb_coupes],dtype='double')
imag_var = np.empty([nb_coupes],dtype='double')


real_var[:] = np.real(debit_freq_fin[:])
imag_var[:] = np.imag(debit_freq_fin[:])

f=open('../DATA/frequentiel/debit_fourier.dat','w')
for i in range (0,nb_capteurs):
        f.write('{:>25.15g}'.format(real_var[i]))
        f.write('{:>25.15g}'.format(imag_var[i]))
        f.write('   \n')
f.close()

