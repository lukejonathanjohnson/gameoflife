#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 21:03:59 2022

@author: lukejohnson1
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import matplotlib.animation as anim
from numpy.fft  import fft2, ifft2
import lifeships as ships

plt.close("all")
"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

Nx = 320
Ny = 384

m = np.zeros((Nx, Ny), int)



class LifePVP():
    
    def __init__(self, Nx=320, Ny=384, bound=32, i1=1, i2=10):
        
        self.__map = np.zeros((Ny, Nx), int)
        self.__i1 = i1
        self.__i2 = i2
        
    def getMap(self, mtype='all'):
        
        m = self.__map
        if mtype=='p1':
            m[m==self.__i2] = 0
        if mtype=='p2':
            m[m==self.__i1] = 0
        if mtype=='o1':
            m[m==self.__i2] = self.__i1
        if mtype=='o2':
            m[m==self.__i1] = self.__i2
            
        return m
    
    def plotMap(self, figname=None, ax=None, ret=False, cmap='plasma'):

        
        if ret==False:
            plt.figure(figname)
            if ax == None:
                ax = plt.subplot(111)
        if ax == None:
            plt.imshow(self.getMap(), cmap=cmap)
        else:
            ax.imshow(self.getMap(), cmap=cmap)
        if ret==True:
            return self.getMap()
        
    
    def addObject(self, obj, i, j, mtype='p1', ud=False):
        
        arr = ships.ships[obj]
        if mtype=='p1':
            arr[arr==1] = self.__i1
        if mtype=='p2':
            arr[arr==1] = self.__i2
        Ni, Nj = np.shape(arr)
        if ud:
            arr = np.flip(arr)
        self.__map[i:i+Ni, j:j+Nj] = arr
        
    def update(self):
        
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        
        c = convolve(self.__map, kernel, mode='constant')
        
        Ni, Nj = np.shape(self.__map)
        
        m2 = self.__map.copy()
        
        
        
        for i in range(Ni):
            for j in range(Nj):
                # if j==0 and map[i]
                    
                
                
                if self.__map[i][j] == 1:
                    
                    if c[i][j]<2 or c[i][j] > 3: #under/overpop
                        m2[i][j] = 0
                    else:
                        pass # lives
                    
                else:
                    if c[i][j] == 3:
                        m2[i][j] = 1 #reproduction
                        
        self.__map = m2
        

    def run(self, N=1, animate=False, figname='ha', cmap='plasma'):
        
        if animate==True:
            fig, ax = plt.figure(figname, figsize=(10, 10)), plt.subplot(111)
            ax.set_xticks([])
            ax.set_yticks([])

            ims = [[ax.imshow(self.getMap(), animated=True, cmap=cmap)]]
            for i in range(N):
                print(str(i+1) + '/' + str(N))
                self.update()
                # img = self.plotMap(ret=True)
                im = ax.imshow(self.getMap(), animated=True, cmap=cmap)
                ims.append([im])

            fig.tight_layout()
            a = anim.ArtistAnimation(fig, ims, interval=100)
            
            return a
                
        else:
            for i in range(N):
                self.update()
                        
def check_and_flip(m, obj):
    pass
                    
                    
                
sim = LifePVP(160, 192)
sim.addObject('coe', 180, 150)
sim.addObject('glider', 150, 20)
sim.addObject('glider', 50, 130)
sim.addObject('lwss', 80, 90)
sim.addObject('loafer', 120, 0)
sim.addObject('copperhead', 100, 40)
sim.addObject('x66', 110, 70)
    


