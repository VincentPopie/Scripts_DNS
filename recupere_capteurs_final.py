# -*- coding: utf-8 -*-
# Vincent Popie (sur la base d'un script de B. Gazanion)

# Ce script permet d'enregistrer de récupérer les données de plusieurs 
# calculs sucessifs et de les enregistrer dans un seul fichier par
# grandeurs.



import numpy as np


#--------------------------------------------------------------------------
nb_capteurs = 104                      # nombre de capteurs  
nb_fichiers = 1                        # nombre de fichiers   
nb_instants = np.array([250])      # nombre d'instants d'ecriture par fichier
nb_instants_tot = nb_instants.sum()
f_ecr = 800                            # Ecriture des capteurs tous les f_ecr cycles

# dossier ou sont ranges les fichiers
dossier='../DATA/'
#--------------------------------------------------------------------------

nb_var = 4;  # nombre de variables
p  = np.zeros([nb_instants_tot,nb_capteurs],'float')  # pression fluctuante
vx = np.zeros([nb_instants_tot,nb_capteurs],'float')  # vitesse fluctuante suivant x
vy = np.zeros([nb_instants_tot,nb_capteurs],'float')  # vitesse fluctuante suivant y
vz = np.zeros([nb_instants_tot,nb_capteurs],'float')  # vitesse fluctuante suivant z
t = np.zeros([nb_instants_tot])

nb_ligne_prec = 0

for num_fichier in range (0,nb_fichiers):    # recuperation des infos fichier par fichier
	#nom_fichier = (dossier+'capteurs/capteur_%d.dat' % (num_fichier+1,)) 
	nom_fichier = (dossier+'capteurs/capteur_final.dat') 
	print ('Fichier : '+nom_fichier+'  -   Nombre de points : %d' % (nb_instants[num_fichier],))

	# ouverture du ficher
	id=open(nom_fichier,'r')

	id.readline()
	id.readline()
	
	for i in range (0,nb_capteurs):

		# Récupération du n° du capteur
		line=id.readline()
		line1=line.split('_')
		line2=line1[1].split(')')
		num_capteur = int(line2[0]) 
		
		# On parcours le fichier pour lire les quatre variables pour le capteur 
		for num_var in range(0,nb_var):

			for num_ligne in range(0,nb_instants[num_fichier]): # On recupere les donnees 

				line = id.readline().split()

			# 1. lecture de la pression fluctuante
				if num_var == 0:
					t[nb_ligne_prec+num_ligne] = line[0]
					p[nb_ligne_prec+num_ligne,num_capteur-1] = line[1]
		
			# 2. lecture de la vitesse fluctuante suivant x
				elif num_var == 1: 
					vx[nb_ligne_prec+num_ligne,num_capteur-1] = line[1]

			# 3. lecture de la vitesse fluctuante suivant y
				elif num_var == 2: 
					vy[nb_ligne_prec+num_ligne,num_capteur-1] = line[1]

			# 4. lecture de la vitesse fluctuante suivant z
				elif num_var == 3:
					vz[nb_ligne_prec+num_ligne,num_capteur-1] = line[1]

			line = id.readline()
			line = id.readline()

			# On ne supprime la ligne 'ZONE ...' que si on n'est pas sur la derniere var
			if not num_var == nb_var-1:
				line = id.readline()
	
	nb_ligne_prec = nb_ligne_prec + nb_instants[num_fichier]
	id.close()

# Ecriture des donnees dans le fichier
for k in range(0,nb_var):
	if k == 0: 
		f=open('../DATA/temporel/pression.dat','w')
	elif k == 1: 
		f=open('../DATA/temporel/vitesse_x.dat','w')
	elif k == 2: 
		f=open('../DATA/temporel/vitesse_y.dat','w')
	elif k == 3: 
		f=open('../DATA/temporel/vitesse_z.dat','w')
	
	for i in range (0,nb_instants_tot):
		f.write('{:>20.15g}'.format(t[i]))
		for j in range (0,nb_capteurs):
			if k==0:
				f.write('{:>20.15g}'.format(p[i,j]))
			if k==1:
				f.write('{:>20.15g}'.format(vx[i,j]))
			if k==2:
				f.write('{:>20.15g}'.format(vy[i,j]))
			if k==3:
				f.write('{:>20.15g}'.format(vz[i,j]))
		f.write('   \n')
	f.close()

