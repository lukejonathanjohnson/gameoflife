#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:00:22 2020

@author: ljj17


"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import healpy as hp
import functools
from skimage.io import imread

plt.close("all")

"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

def sin(x):
    return np.sin(np.deg2rad(x))

def arcsin(x):
    return np.rad2deg(np.arcsin(x))


class GameOfLife():
    """
    Class for a HealPix map
    """
    def __init__(self, res):
        if (res < 1) or (res > 30):
            raise Exception("resolution must be an integer between 1 and 30")
        
        self.res = res
        self.nside = 2**res
        self.npix = hp.nside2npix(self.nside)
        self.map = np.linspace(0, 0, self.npix)
        self.v2p = functools.partial(hp.vec2pix, hp.npix2nside(len(self.map)))
    
    
    def addpc(self, pc, seed=None):
        
        np.random.seed(seed)
        
        N = len(self.map)
        
        on = int(N * pc / 100)
        
        
        selected = np.random.choice(np.arange(N), on)
        
        self.map[selected] = 1
        
    def GetMap(self):
        return self.map
    
    def plotmap(self, figname=None, proj='orthographic', rot=[0, 90], xsize=1000,
                ax=None, halfsky=False, ret=False, cmap='plasma', pad='default'):

        if pad=='default':
            pad = int(xsize/16)
        
        rot = [-rot[0], rot[1]-90]
        
        if ret==False:
            plt.figure(figname)
            if ax == None:
                ax = plt.subplot(111)
        
        if proj=='cartesian':
            star = hp.projector.CartesianProj(xsize=xsize).projmap(self.map, self.v2p)
            if ret==True:
                return star
            ax.imshow(star, extent=(0, 360, -90, 90))
            plt.yscale('function', functions=(sin, arcsin))
            yt = [-90, -60, -30, 0, 30, 60, 90]
            xt = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
            plt.yticks(yt, fontsize=16)
            plt.xticks(xt, fontsize=16)
            plt.xlabel(r'Longitude [$^\circ$]', fontsize=26)
            plt.ylabel(r'Latitude [$^\circ$]', fontsize=26)
            for i in yt[1:-1]:
                ls='--'
                if i == 0:
                    ls='-'
                plt.axhline(i, ls=ls, color='black', lw=1, alpha=0.5)
                    
            for j in xt[1:-1]:
                ls='--'
                if j % 90 == 0:
                    ls='-'
                plt.axvline(j, ls=ls, color='black', lw=1, alpha=0.5)
        
        elif proj == 'orthographic':
            star = hp.projector.OrthographicProj(rot=rot, half_sky=halfsky, xsize=xsize).projmap(self.map, self.v2p)
            star[star == -np.inf] = -1
        
            star = np.pad(star, pad_width=pad, mode='constant', constant_values=-1)
            
            if ret==True:
                return star
            ax.imshow(star, cmap=cmap)
        
            
    
    def countliveneighbours(self, pix, retn=False):
        
        neighbours = hp.get_all_neighbours(self.nside, pix)
        liven = int(np.sum(self.map[neighbours]))
        
        if retn==True:
            return neighbours
        else:
            return liven
    
    def applyrules(self, pix):
        
        LN = self.countliveneighbours(pix)
        
        if self.map[pix] == 1: #live cells
            
            if LN < 2:
                self.map[pix] = 0 #underpopulation
            
            if LN > 3:
                self.map[pix] = 0 #overpopulation
                
        elif self.map[pix] == 0: #dead cells
            
            if LN == 3:
                self.map[pix] = 1 #reproduction
    
    def timestep(self):
        
        N = len(self.map)
        
        for i in range(N):
            self.applyrules(i)
    
    def run(self, N=1, animate=False, figname='ha', cmap='plasma', halfsky=False, xsize=2000, rotate=False, rotinit=0, inc=90, pad='default'):
        
        if animate==True:
            fig, ax = plt.figure(figname, figsize=(10, 5)), plt.subplot(111)
            ax.set_xticks([])
            ax.set_yticks([])

            ims = [[ax.imshow(self.plotmap(ret=True, halfsky=halfsky, xsize=xsize, rot=[rotinit, inc]), animated=True, cmap=cmap)]]
            for i in range(N):
                if rotate:
                    rotinit += 1
                print(str(i+1) + '/' + str(N))
                self.timestep()
                star = self.plotmap(ret=True, halfsky=halfsky, xsize=xsize, rot=[rotinit, inc])
                im = ax.imshow(star, animated=True, cmap=cmap)
                ims.append([im])

            fig.tight_layout()
            a = anim.ArtistAnimation(fig, ims, interval=100)
            
            return a
                
        else:
            for i in range(N):
                self.timestep()
        
        
        
            
def plotgrid(figname=None):
    
    sim = GameOfLife(6)
    sim.addpc(20, 54321)
    
    
    
    
    fig = plt.figure(figname, figsize=(8, 10))
    rotinit=0
    
    for i in range(20):
        sim.timestep()
        ax = plt.subplot(5, 4, i+1)
        sim.plotmap(figname, ax=ax, halfsky=True, pad=10, cmap='inferno', rot=[rotinit, 80])
        plt.xticks([])
        plt.yticks([])
        rotinit+=1
        
    fig.savefig('hahahaha.png')
    

def starpeopleimg():

    im = imread('/Users/lukejohnson1/Dropbox/Luke/Illustration/starpeopletext_clean.png')
        
    N = len(im)
    M = len(im[0])
    
    immy = np.zeros((N, M))
    
    for i in range(N):
        for j in range(M):
            immy[i][j] = im[i][j].sum()
    
    immy[immy > 0] = 1
    return immy


def gameoflife(im):
    
    N = len(im)
    M = len(im[0])
    
    im2 = np.zeros((N, M))
    
    for x in range(N):
        for y in range(M):
            LN = np.sum(im[x - 1:x + 2, y - 1:y + 2]) - im[x, y]
            
            if im[x][y] == 1:
                
                if LN < 2:
                    im2[x][y] = 0 #underpopulation
                
                if LN > 3:
                    im2[x][y] = 0 #overpopulation
                    
            elif im[x][y] == 0: #dead cells
                
                if LN == 3:
                    im2[x][y] = 1 #reproduction
    
    return im2
    

        
        