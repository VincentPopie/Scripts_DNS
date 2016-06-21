# -*- coding: utf-8 -*-
# Vincent Popie

# Calcule l'impedance a partir des pressions et vitesses mesurees

import numpy as np
import scipy.fftpack as fft
import matplotlib.pyplot as plt

from trace_pression_vitesse import *


##########################
## Parametres physiques ##
##########################

freq = 5000.0
omega = 2*np.pi*freq
R = 287.058
gamma = 1.4
T = 288.0
c = np.sqrt(gamma*R*T)
c = 340.0
k = omega / c
print('c, k : ', c, k)
lambdal = c / freq
rho = 1.204


#########################
## Lecture des données ##
#########################

data = np.loadtxt('../DATA/frequentiel/pression.dat')
x=data[:,0]
pression = data[:,1] + 1j*data[:,2]

databis = np.loadtxt('../DATA/frequentiel/vitesse_z.dat')
vitesse =  databis[:,1] + 1j*databis[:,2]

N = len(x) 

xp = -0.0005 #Centre de la perforation




########################################
## Selection des points moindre carre ##
########################################

ind_gauche = np.arange(22,26)
ind_droite = np.arange(N-21,N-17)
x_gauche =  x[ind_gauche] - xp
x_droite = x[ind_droite] - xp



#####################################
### Construction du second membre ###
#####################################

rhs_gauche = np.empty([np.size(ind_gauche)*2], 'complex')
rhs_gauche[:np.size(ind_gauche)]=pression[ind_gauche]
rhs_gauche[np.size(ind_gauche):]=vitesse[ind_gauche]

rhs_droite = np.empty([np.size(ind_droite)*2], 'complex')
rhs_droite[:np.size(ind_droite)]=pression[ind_droite]
rhs_droite[np.size(ind_droite):]=vitesse[ind_droite]


#################################
### Construction des matrices ###
#################################
matrice_gauche = np.empty([np.size(ind_gauche)*2,2], 'complex')
matrice_gauche[:np.size(ind_gauche),0] = np.exp(1j*k*x_gauche)
matrice_gauche[:np.size(ind_gauche),1] = np.exp(-1j*k*x_gauche)
matrice_gauche[np.size(ind_gauche):,0] = -np.exp(1j*k*x_gauche)/rho/c
matrice_gauche[np.size(ind_gauche):,1] = np.exp(-1j*k*x_gauche)/rho/c

matrice_droite = np.empty([np.size(ind_droite)*2,2], 'complex')
matrice_droite[:np.size(ind_droite),0] = np.exp(1j*k*x_droite)
matrice_droite[:np.size(ind_droite),1] = np.exp(-1j*k*x_droite)
matrice_droite[np.size(ind_droite):,0] = -np.exp(1j*k*x_droite)/rho/c
matrice_droite[np.size(ind_droite):,1] = np.exp(-1j*k*x_droite)/rho/c



####################################
## Resolution des moindres carres ##
####################################
# le vecteur rhs contient mes donnees
# matrice contient le modele

# la fonction lstsq de numpy.linalg
# resout min Ax - b au sens des moindres carres


result_gauche = np.linalg.lstsq(matrice_gauche, rhs_gauche)[0]
reste_gauche = np.linalg.lstsq(matrice_gauche, rhs_gauche)[1]
A = result_gauche[0]
B = result_gauche[1]

result_droite = np.linalg.lstsq(matrice_droite, rhs_droite)[0]
reste_droite = np.linalg.lstsq(matrice_droite, rhs_droite)[1]

C = result_droite[0]
D = result_droite[1]



###############################
### Affichage des solutions ###
###############################


print

print("Solution de l'onde plane : ")
print('A : ', A)
print('B : ', B)
print('C : ', C)
print('D : ', D)


#############################
### Affichage des résidus ###
#############################

print
print('Les résidus sont normalisés par la norme du vecteur de mesures')
print('residu_gauche :', reste_gauche/np.linalg.norm(rhs_gauche))
print('residu_droite :', reste_droite/np.linalg.norm(rhs_droite))



############################################################
### Calcul des coefficients de reflexion et transmission ###
############################################################
xh = 0.0005

xp_gauche =  + xh
xp_droite =  - xh

Reflexion_epaisse = B/A*np.exp(-2j*k*xh)
Transmission_epaisse = C/A

print('x_gauche : ', xp_gauche)
print('x_droite : ', xp_droite)
print
print('Coefficient de reflexion : ', Reflexion_epaisse)
print('Coefficient de transmission :', Transmission_epaisse)
print('A = 1 - R - T = ', 1 - Reflexion_epaisse - Transmission_epaisse)



#############################
### Calcul de l'impedance ###
#############################

Impedance_R_epaisse = (2*Reflexion_epaisse)/(1-Reflexion_epaisse)
Impedance_T_epaisse = (2-2*Transmission_epaisse)/Transmission_epaisse

print
print('Impedance epaisse, Reflexion et Transmission:', Impedance_R_epaisse, Impedance_T_epaisse)

print
print(' Verif condition : ')
print('Reflexion + Transmission, epaisse et fine : ', Reflexion_epaisse + Transmission_epaisse)
print('Amplitude, epaisse et fine : ', np.abs(Reflexion_epaisse + Transmission_epaisse))
print('Phase, epaisse et fine : ', np.angle(Reflexion_epaisse + Transmission_epaisse)/k)



#############################
### CALCUL DES INTENSITES ###
#############################

#I_1 = 1.0/2.0*np.real(p_gauche*np.conj(v_gauche))
#I_1_plus = 1.0/2.0*np.real(p_gauche_plus*np.conj(v_gauche_plus))
#I_1_moins = 1.0/2.0*np.real(p_gauche_moins*np.conj(v_gauche_moins))
#I_2_plus = 1.0/2.0*np.real(p_droite*np.conj(v_droite))
absorption = 1 -  np.abs(Reflexion_epaisse)* np.abs(Reflexion_epaisse) \
               - np.abs(Transmission_epaisse)* np.abs(Transmission_epaisse)

#print('Intensité',I_1)
print('Absorption :', absorption)


########
# Plot #
########
plot_pression_vitesse(x, pression, vitesse, ind_gauche, ind_droite,
                      A, B, C, k, rho, c, xp_droite)
                      
plot_manuscrit(x, pression, vitesse, ind_gauche, ind_droite,
                      A, B, C, k, rho, c, xp_droite)