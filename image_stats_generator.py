# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:37:01 2024

@author: rasmu
"""

# Generate stats (SNR, FT_SNR, etc...)

# inspiration from 

# calculate SNR form Fourier Space
import numpy as np
import scipy.fftpack as fft
import cv2

def calculate_snr_frequency_domain(image):
    # Convert to grayscale if necessary
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    # Perform Fourier Transform
    f_image = fft.fft2(gray_image)

    # Shift zero-frequency component to center
    f_shifted = fft.fftshift(f_image)

    # Calculate power spectrum
    power_spectrum = np.abs(f_shifted)**2

    # Define a threshold to separate signal and noise (adjust as needed)
    threshold = np.mean(power_spectrum)

    # Create masks for signal and noise regions
    signal_mask = power_spectrum > threshold
    noise_mask = power_spectrum <= threshold

    # Calculate power of signal and noise
    power_signal = np.sum(power_spectrum[signal_mask])
    power_noise = np.sum(power_spectrum[noise_mask])

    # Calculate SNR
    ft_snr = power_signal / power_noise

    return ft_snr

def calculate_simple_snr(image):
    # consider implementing signal and noise regions
    
    # Convert to grayscale if necessary
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
        
    snr_basic = np.mean(gray_image)/np.std(gray_image)
    return snr_basic

