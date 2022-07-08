from unittest import result
import cv2
from cv2 import exp
import numpy as np
from matplotlib import pyplot as plt

class filter:
    def __init__(self, cutoff):
        self.cutoff = cutoff
        self.n = 2      # Default
        self.rows = 250  # Default
        self.cols = 250  # Default

    def updateImage(self, img):
        
        self.rows, self.cols = img.shape

    def computeDuv(self):
        
        crow, ccol = self.rows//2 , self.cols//2              # Define center point of image
        r, c = np.mgrid[0:self.rows:1, 0:self.cols:1]
        c -= crow
        r -= ccol
        return np.sqrt(np.power(r, 2.0) + np.power(c, 2.0)) # Define center positioned circular filter
        
    def computeH(self, ftype, ptype, d, d0, n=2):
        
        if ftype == "ideal":
            return self.computeIdeal(ptype, d, d0, n)
        elif ftype == "butterworth":
            return self.computeButterworth(ptype, d, d0, n)
        elif ftype == "gaussian":
            return self.computeGaussian(ptype, d, d0)
    
    def computeIdeal(self, ptype, d, d0, n):
            # ptype: Pass type
            # d: D(u,v)
            # d0: cutoff frequence
 
            if (ptype == "lpf"):
                H = (d>=d0)
            elif (ptype == "hpf"):
                H = (d<=d0)
            return H
    
    def computeButterworth(self, ptype, d, d0, n):

        if (ptype == "hpf"):
            H = 1.0 / (1 + np.power(d/d0, 2*n))
        elif (ptype == "lpf"):
            H = 1.0/(1 + np.power(d0/d, 2*n)) 
        return H

    def computeGaussian(self, ptype, d, d0):

        if (ptype == "lpf"):
            H = exp(-np.power(d0, 2)/(2*np.power(d, 2)))
        elif (ptype == "hpf"):
            H = exp(-np.power(d, 2)/(2*np.power(d0, 2)))  
        return H
    
    def applyFilter(self, F,H):
        H_M = np.zeros((self.rows, self.cols, 2), np.float32)
        H_M[:, :, 0] = H
        H_M[:, :, 1] = H
        return F*H_M
    
    def computeInverseFFT(self, fftimg):
        
        f_ishift = np.fft.ifftshift(fftimg)
        filtered_img = cv2.idft(f_ishift)
        result = cv2.magnitude(filtered_img[:,:,0],filtered_img[:,:,1])
        return result

    def computeFFT(self, img):

        dft =cv2.dft(img,flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift=np.fft.fftshift(dft)
        return dft_shift