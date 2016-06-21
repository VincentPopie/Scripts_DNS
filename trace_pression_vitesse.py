# -*- coding: utf-8 -*-
# Vincent Popie

import numpy as np
import matplotlib.pyplot as plt

def plot_pression_vitesse (x, pression, vitesse, ind_gauche, ind_droite, 
                           A, B, C, 
                           k, rho, c, xp_droite):
	C1 = C*np.exp(-1j*k*(xp_droite))

	xabs_gauche = np.linspace(0.136,0,5001)
	xabs_droite = np.linspace(-0.001,-0.051,5001)

	p_gauche =  A*np.exp(1j*k*xabs_gauche) + B*np.exp(-1j*k*xabs_gauche)
	p_gauche_plus =  A*np.exp(1j*k*xabs_gauche)
	p_gauche_moins =  B*np.exp(-1j*k*xabs_gauche)


	p_droite =  C*np.exp(1j*k*xabs_droite) #+ D*np.exp(-1j*k*xabsdroite) 

	v_gauche =  -A*np.exp(1j*k*xabs_gauche)/rho/c + B*np.exp(-1j*k*xabs_gauche)/rho/c
	v_gauche_plus =  -A*np.exp(1j*k*xabs_gauche)/rho/c
	v_gauche_moins =  B*np.exp(-1j*k*xabs_gauche)/rho/c


	v_droite =  -C*np.exp(1j*k*xabs_droite)/rho/c #+ D*np.exp(-1j*k*xabsdroite)/rho/c
	v_droitebis =  -C1*np.exp(1j*k*xabs_droite)/rho/c #+ D*np.exp(-1j*k*xabsdroite)/rho/color


	# Partie reelle de la pression
	plt.figure(4)
	plt.plot(x,np.real(pression), 'o', 
	     	 xabs_gauche, np.real(p_gauche),
	         xabs_droite,np.real(p_droite))

	plt.axvline(x=0.00, color='k')
	plt.axvline(x=-0.001, color='k')

	plt.axvline(x=x[ind_gauche[0]], color='g')
	plt.axvline(x=x[ind_gauche[-1]], color='g')
	plt.axvline(x=x[ind_droite[0]], color='r')
	plt.axvline(x=x[ind_droite[-1]], color='r')
	plt.xlim([0.140,-0.06])

	# Partie imaginaire de la pression
	plt.figure(5)
	plt.plot(x,np.imag(pression), 'o', 
		 	 xabs_gauche, np.imag(p_gauche),
		     xabs_droite,np.imag(p_droite))

	plt.axvline(x=0.00, color='k')
	plt.axvline(x=-0.001, color='k')

	plt.axvline(x=x[ind_gauche[0]], color='g')
	plt.axvline(x=x[ind_gauche[-1]], color='g')
	plt.axvline(x=x[ind_droite[0]], color='r')
	plt.axvline(x=x[ind_droite[-1]], color='r')
	plt.xlim([0.140,-0.06])


	# Partie reelle de la vitesse
	plt.figure(6)
	plt.plot(x,np.real(vitesse), 'o', 
	     	 xabs_gauche, np.real(v_gauche),
	         xabs_droite,np.real(v_droite),
	         xabs_droite,np.real(v_droitebis))

	plt.axvline(x=0.00, color='k')
	plt.axvline(x=-0.001, color='k')

	plt.axvline(x=x[ind_gauche[0]], color='g')
	plt.axvline(x=x[ind_gauche[-1]], color='g')
	plt.axvline(x=x[ind_droite[0]], color='r')
	plt.axvline(x=x[ind_droite[-1]], color='r')

	plt.xlim([0.140,-0.06])


	# Partie imaginaire de la vitesse
	plt.figure(7)
	plt.plot(x,np.imag(vitesse), 'o', 
			 xabs_gauche, np.imag(v_gauche),
			 xabs_droite, np.imag(v_droite),
			 xabs_droite,np.imag(v_droitebis))

	plt.axvline(x=0.00, color='k')
	plt.axvline(x=-0.001, color='k')

	plt.axvline(x=x[ind_gauche[0]], color='g')
	plt.axvline(x=x[ind_gauche[-1]], color='g')
	plt.axvline(x=x[ind_droite[0]], color='r')
	plt.axvline(x=x[ind_droite[-1]], color='r')
	plt.xlim([0.140,-0.06])


plt.show()
plt.close('all')



def plot_manuscrit(x, pression, vitesse, ind_gauche, ind_droite, 
                   A, B, C, k, rho, c, xp_droite):

	xabs_gauche = np.linspace(0.136,0,5001)
	xabs_droite = np.linspace(-0.001,-0.051,5001)


	ind_graphe = np.empty([95],dtype='int')
	ind_graphe[1:-3] = np.arange(8,99)
	ind_graphe[0]= 3
	ind_graphe[-3]= 99
	ind_graphe[-2]= 101
	ind_graphe[-1]= 103
	x_graphe = x[ind_graphe]
	x_graphe = -x_graphe

	xabs_gauche = -xabs_gauche
	xabs_droite = -xabs_droite

	p_gauche =  A*np.exp(-1j*k*xabs_gauche) + B*np.exp(1j*k*xabs_gauche)
	p_droite =  C*np.exp(-1j*k*xabs_droite) #+ D*np.exp(-1j*k*xabsdroite) 

	v_gauche =  -A*np.exp(1j*k*xabs_gauche)/rho/c + B*np.exp(-1j*k*xabs_gauche)/rho/c
	v_droite =  -C*np.exp(1j*k*xabs_droite)/rho/c

	params = {'legend.fontsize': 20}
	plt.rcParams.update(params)

	# Partie reelle de la pression
	plt.figure(21, figsize=(10,8), dpi=200)

	plt.plot(x_graphe,np.real(pression[ind_graphe]), 'o', label=r'$p$')
	plt.plot(xabs_gauche, np.real(p_gauche),'--',linewidth=3, label=r'$\tilde{p}_I$')
	plt.plot(xabs_droite,np.real(p_droite),'-',linewidth=3, label=r'$\tilde{p}_{II}$')

	plt.legend(fontsize=25)
	plt.xlabel(r'$x_1$',fontsize=30)
	plt.ylabel(r'$\Re(p)$',fontsize=30)
	plt.xlim([-0.140,0.06])
	plt.rc('font', size=20)

	plt.axvline(x=0.00, color='k', linestyle=':',linewidth=2)
	plt.axvline(x=0.001, color='k', linestyle=':',linewidth=2)

	plt.savefig('../Figure/pression_re.jpeg', format='jpeg', bbox_inches='tight',
				pad_inches=0.2, dpi=300, quality=95 )


	# Partie imaginaire de la pression
	plt.figure(22, figsize=(10,8), dpi=200)

	plt.plot(x_graphe,np.imag(pression[ind_graphe]), 'o', label=r'$p$')
	plt.plot(xabs_gauche, np.imag(p_gauche),'--',linewidth=3, label=r'$\tilde{p}_I$')
	plt.plot(xabs_droite, np.imag(p_droite),'-',linewidth=3, label=r'$\tilde{p}_{II}$' )

	plt.legend(fontsize=25)
	plt.xlabel(r'$x_1$',fontsize=30)
	plt.ylabel(r'$\Im(p)$',fontsize=30)
	plt.xlim([-0.140,0.06])
	plt.rc('font', size=20)

	plt.axvline(x=0.00, color='k', linestyle=':',linewidth=2)
	plt.axvline(x=0.001, color='k', linestyle=':',linewidth=2)


	plt.savefig('../Figure/pression_im.jpeg', format='jpeg', bbox_inches='tight',
				pad_inches=0.2, dpi=300, quality=95 )

	# Partie reelle de la pression zoom
	plt.figure(23, figsize=(10,8), dpi=200)

	plt.plot(x_graphe,np.real(pression[ind_graphe]), 'o', label=r'$p$')
	plt.plot(xabs_gauche, np.real(p_gauche),'--',linewidth=3, label=r'$\tilde{p}_I$')
	plt.plot(xabs_droite,np.real(p_droite),'-',linewidth=3, label=r'$\tilde{p}_{II}$' )

	plt.legend(loc=4,fontsize=25)
	plt.xlabel(r'$x_1$',fontsize=30)
	plt.ylabel(r'$\Re(p)$',fontsize=30)
	plt.xlim([-0.05,0.05])
	plt.rc('font', size=20)  

	plt.axvline(x=0.00, color='k',  linestyle=':')
	plt.axvline(x=0.001, color='k', linestyle=':')

	plt.savefig('../Figure/pression_re_2.jpeg', format='jpeg', bbox_inches='tight',
				pad_inches=0.2, dpi=300, quality=95 )


	# Partie imaginaire de la pression zoom
	plt.figure(24, figsize=(10,8), dpi=200)

	plt.plot(x_graphe,np.imag(pression[ind_graphe]), 'o', label=r'$p$')
	plt.plot(xabs_gauche, np.imag(p_gauche),'--',linewidth=3, label=r'$\tilde{p}_I$')
	plt.plot(xabs_droite,np.imag(p_droite),'-',linewidth=3, label=r'$\tilde{p}_{II}$')

	plt.legend(fontsize=25)
	plt.xlabel(r'$x_1$',fontsize=30)
	plt.ylabel(r'$\Im(p)$',fontsize=30)
	plt.xlim([-0.05,0.05])
	plt.rc('font', size=20)  

	plt.axvline(x=0.00, color='k', linestyle=':')
	plt.axvline(x=0.001, color='k', linestyle=':')

	plt.savefig('../Figure/pression_im_2.jpeg', format='jpeg', bbox_inches='tight',
				pad_inches=0.2, dpi=300, quality=95 )


	# Calcul des intensites
	I_1 = 1.0/2.0*np.real(p_gauche*np.conj(v_gauche))
	I_2 = 1.0/2.0*np.real(p_droite*np.conj(v_droite))
	I_m = 1.0/2.0*np.real(pression[ind_graphe]*np.conj(vitesse[ind_graphe]))

	# Trace des intensites
	plt.figure(25, figsize=(10,8), dpi=200)

	plt.plot(x_graphe,I_m, 'o', label=r'$I$')
	plt.plot(xabs_gauche, I_1,'--',linewidth=3, label=r'$\tilde{I}_I$')
	plt.plot(xabs_droite, I_2,'-',linewidth=3, label=r'$\tilde{I}_{II}$' )

	plt.legend(loc=4,fontsize=25)
	plt.xlabel(r'$x_1$',fontsize=30)
	plt.ylabel(r'$I$',fontsize=30)
	plt.xlim([-0.136,0.05])
	plt.rc('font', size=20)

	plt.axvline(x=0.00, color='k', linestyle=':')
	plt.axvline(x=0.001, color='k', linestyle=':')

	plt.savefig('../Figure/intensite.jpeg', format='jpeg', bbox_inches='tight',
				pad_inches=0.2, dpi=300, quality=95 )
	plt.show()


