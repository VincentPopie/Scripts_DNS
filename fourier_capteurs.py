# -*- coding: utf-8 -*-
# Vincent Popie

# Calcul de la FFT des pressions et vitesses

import numpy as np
import scipy.fftpack as fft
import matplotlib.pyplot as plt


nb_capteurs = 104

###########################
## Position des capteurs ##
###########################

Nperfo = 50
x_perfo_init = 0.002
x_perfo_fin = -0.003
x_perfo = np.linspace(x_perfo_init, x_perfo_fin, Nperfo+1)

Navant = 18
x_avant_init = 0.1292
x_avant_fin = 0.0068
x_avant = np.linspace(x_avant_init, x_avant_fin, Navant+1)

Napres = 17
x_apres_init = -0.0035
x_apres_fin = -0.046
x_apres = np.linspace(x_apres_init, x_apres_fin, Napres+1)

Ndebut = 6
x_debut_init = 0.136
x_debut_fin = 0.130
x_debut = np.linspace(x_debut_init, x_debut_fin, Ndebut+1)

Nmilieu = 3
x_milieu_init = 0.006
x_milieu_fin = 0.003
x_milieu = np.linspace(x_milieu_init, x_milieu_fin, Nmilieu+1)

Nfin = 4
x_fin_init = -0.047
x_fin_fin = -0.051
x_fin = np.linspace(x_fin_init, x_fin_fin, Nfin+1)

N = Nperfo + Navant + Napres + Ndebut + Nmilieu + Nfin + 6
x = np.empty(N,'double')
x[0 : Ndebut+1] = x_debut[:]
x[Ndebut+1 : Ndebut+Navant+2] = x_avant[:]
x[Ndebut+Navant+2 : Ndebut+Navant+Nmilieu+3] = x_milieu[:]
x[Ndebut+Navant+Nmilieu+3 : Ndebut+Navant+Nmilieu+Nperfo+4] = x_perfo[:]
x[Ndebut+Navant+Nmilieu+Nperfo+4 : Ndebut+Navant+Nmilieu+Nperfo+Napres+5] = x_apres[:]
x[Ndebut+Navant+Nmilieu+Nperfo+Napres+5 : Ndebut+Navant+Nmilieu+Nperfo+Napres+Nfin+6] = x_fin[:]

#########################
## Lecture des données ##
#########################

data = np.loadtxt('../DATA/temporel/pression.dat')
t=data[:,0]
pression = data[:,1:nb_capteurs+1]

data = np.loadtxt('../DATA/temporel/vitesse_z.dat')
vitesse = data[:,1:nb_capteurs+1]


###########################
## Préparation de la FFT ##
###########################

dt = t[1]-t[0]

print 
print
print('Pas de temps : ', dt, t[1], t[0])
print('Frequence : 5000 Hz')
print("Longueur d'onde : ", 340.0/5000)
print("Periode :" , 1.0/5000)
print('Tfin : ', 10.0/5000, t[-1])
print 


idebut = int(6.0/5000/dt)  - int(5.0/5000/dt)
ifin = len(t) - 1
print("Iteration du debut : ", t[idebut], pression[idebut,11])
print("Iteration de fin : ", t[ifin], pression[ifin,11])


t_fourier = t[idebut:ifin+1]

pression_fourier = pression[idebut:ifin+1,:]
pression_mean = np.mean(pression_fourier, axis=0)

vitesse_fourier = vitesse[idebut:ifin+1,:]
vitesse_mean = np.mean(vitesse_fourier, axis=0)


print('Taille de pression_mean : ', len(pression_mean))

# On supprime les valeurs moyennes pour ne garder que les valeurs fluctuantes
for i in range(0,nb_capteurs):
	pression_fourier[:,i] = pression_fourier[:,i] - pression_mean[i]
	vitesse_fourier[:,i] = vitesse_fourier[:,i] - vitesse_mean[i]

N = len(t_fourier)
f = fft.fftfreq(N,dt)
print('Fréquences : ', f)

y = np.empty([N,nb_capteurs],dtype = 'complex')
y_vit = np.empty([N,nb_capteurs],dtype = 'complex')

for i in range(0,nb_capteurs):
	y[:,i] = fft.fft(pression_fourier[:,i])
	y_vit[:,i] = fft.fft(vitesse_fourier[:,i])


#indice = np.argmax(np.abs(y),axis=0)

# Multiplication par le bon facteur
m = 2.0/N*y[4,:]
m_vit = 2.0/N*y_vit[4,:]

###########################
# Ecriture des solutions ##
###########################
real_m = np.empty([nb_capteurs],dtype='double')
imag_m = np.empty([nb_capteurs],dtype='double')
real_m[:] = np.real(m[:])
imag_m[:] = np.imag(m[:])

real_m_vit = np.empty([nb_capteurs],dtype='double')
imag_m_vit = np.empty([nb_capteurs],dtype='double')
real_m_vit[:] = np.real(m_vit[:])
imag_m_vit[:] = np.imag(m_vit[:])


f=open('../DATA/frequentiel/pression.dat','w')
f2=open('../DATA/frequentiel/vitesse_z.dat','w')
for i in range (0,nb_capteurs):
	f.write('{:>20.15g}'.format(x[i]))
	f2.write('{:>20.15g}'.format(x[i]))
 
	f.write('{:>25.15g}'.format(real_m[i]))
	f.write('{:>25.15g}'.format(imag_m[i]))
	f2.write('{:>25.15g}'.format(real_m_vit[i]))
	f2.write('{:>25.15g}'.format(imag_m_vit[i]))

	
	f.write('   \n')
	f2.write('   \n')

f.close()
f2.close()
