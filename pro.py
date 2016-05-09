# -*- coding: utf-8 -*-
#!/usr/bin/env python
#<Friendly-memory>
#Copyright (C) <2017>  <Morgane Chassagne & Alexia Aigloz>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame #importation de la librairie
from random import shuffle  #script pour melanger

#tailles
nbcellsx = 5 #nbr cases horizontalement
nbcellsy = 4 #nbr cases verticalement
cellsize = 160 #taille d'une carte
#symboles 
set_ = list("0123456789") #liste

#couleurs
bg = pygame.Color("white") #background
nbr = pygame.Color("black") #chiffres noir
dos = pygame.Color("0x484848") #dos gris
face = pygame.Color("white") #face non valide
rej = pygame.Color("black") #rejouer
after = pygame.Color("0x2bd1b3")#validé bleu

#Initialisation
scr = pygame.display.set_mode((nbcellsx*cellsize,nbcellsy*cellsize))
scrrect = scr.get_rect()
pygame.font.init() #determine taille police en fonction taille cases
police = pygame.font.Font(None,int(cellsize//1.5))
firstcard = None # memorise l'index de la 1ere carte retournee par tour

def melange(): 
    nb_cartes = (nbcellsx*nbcellsy)//2
    cartes = set_*int(nb_cartes//len(set_))
    cartes += set_[:nb_cartes%len(set_)]
    cartes *= 2
    shuffle(cartes)
    return cartes

def face_cachee():  
    scr.fill(bg)
    for y in range(0,scrrect.h,cellsize):
        for x in range(0,scrrect.w,cellsize):
            scr.fill(dos,(x+1,y+1,cellsize-2,cellsize-2))
    pygame.display.flip()

def rejouer(): 
    mess = police.render('Rejouer ? Clique !',1,bg,after)
    pygame.display.update(scr.blit(mess,mess.get_rect(center=scrrect.center)))
    while True:
		ev = pygame.event.wait()
		if ev.type   == pygame.MOUSEBUTTONDOWN: return True
		elif ev.type == pygame.QUIT: return False

while True:
    cartes = melange()
    face_cachee()
    pygame.event.clear()
    pygame.time.set_timer(pygame.USEREVENT,1000)
    secondes = 0 # lance le chrono

    while any(cartes):# les paires trouvees sont misent a  None dans cartes donc, temps que cartes ne contient pas que des None
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT: break # quitte le jeu
        elif ev.type == pygame.USEREVENT:
            secondes += 1  # update le chrono
            pygame.display.set_caption(str(secondes))
        elif ev.type == pygame.MOUSEBUTTONDOWN:            
            index = ev.pos[1]//cellsize*nbcellsx+ev.pos[0]//cellsize # la position de la souris est convertie en index dans cartes
            if cartes[index] and index!=firstcard: # si la carte n'est pas retournee on la retourne en coloriant sa position               
                r = scr.fill(face,(index%nbcellsx*cellsize+1,index//nbcellsx*cellsize+1,cellsize-2,cellsize-2)) # r memorise l'emplacement sur l'ecran
                motif = police.render(str(cartes[index]),1,nbr)               
                scr.blit(motif,motif.get_rect(center=(r.center))) # on affiche le symbole au centre
                pygame.display.update(r)
                if firstcard is None: # si vrai alors c'est la premiere carte que l'on retourne dans ce tour
                    firstcard = index # memorise la valeur
                    firstr = r # et l'emplacement
                    continue
                # sinon ...si les 2 cartes sont identiques on les "devoilent" dans cartes valeurs a None
                if cartes[index] == cartes[firstcard]:
                    scr.fill(after,r,special_flags=pygame.BLEND_MIN)
                    scr.fill(after,firstr,special_flags=pygame.BLEND_MIN)
                    pygame.time.wait(500)
                    pygame.display.update((r,firstr))
                    cartes[index] = cartes[firstcard] = None
                else: # sinon ...
                    pygame.time.wait(500)                   
                    pygame.display.update((scr.fill(dos,r),scr.fill(dos,firstr)))# on les re-cache en les coloriant
                firstcard = None
    else:
        pygame.time.wait(500)
        if rejouer(): continue
    break

pygame.quit()
