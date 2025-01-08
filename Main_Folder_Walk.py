# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:37:15 2024

@author: svw191
"""

# Main: Pick the upper parent folder and walk through all subfolders

## STEP 1: check if stack has been made, make STK
## STEP 2: check if average has been made, make average .tif file


# Function is checking if the target folder is available, and if not,it leaves it with a message.
# This avoids any overwriting or data-mixing.


# Folder selection
import tkinter as tk
from tkinter import filedialog
import os

# Image-reading
import imageio
import tifffile
import numpy as np
import time
from matplotlib import pyplot as plt
# External codes
from Thorlabs_tif_stks import read_tif_stack, stack_tif_images, tif2png
from image_stats_generator import calculate_snr_frequency_domain, calculate_simple_snr

# define the variables to look for:
chans = ['ChanA','ChanB'] # make it applicable for both 1- and 2-color imaging

# Select a folder
root = tk.Tk()
root.withdraw()  # Hide the main window

rtdir = filedialog.askdirectory()
if rtdir:
    print(f"Selected folder: {rtdir}")

# First Approach: Run through iterative search in each sub-branch of the folder
# Identify the folder containing .tif files. If there are ChanA-images, check for "DATA\\ChanA"-folder. Equally with "ChanB".
# Create folder, if they do not exist. Check if existing folders are empty, if so, generate the .tif-stack.

for root, _, files in os.walk(rtdir):
    for chan in chans: # waking independently in each channel
        if f"{chan}_001_001_001_001.tif" in files:
            # Prepare DATA-folder if not already made
            chandir = os.path.join(root, 'DATA', chan)
            if not os.path.isdir(chandir): 
                os.makedirs(chandir)                                                              
                
            ## STEP 1: check if stack has been made, make STK
            # NB: this just checks if the folder is empty
            
            if len(os.listdir(chandir)) == 0:
                print(f"{chandir} is empty")
                
                start_time = time.time()
                
                stack_tif_images(root, chan)
                print("Stack has been completed")
                
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                print("Elapsed time:", elapsed_time, "seconds")
                
            ## STEP 2: check if average has been made, make average .tif file
            # Step 2a: Make the average .tif file from STK
            # Step 2b: Make the .png from that 
            # NB: check .png file, not .jpg
            if not os.path.isfile(os.path.join(chandir, f"{chan}_stk_avg.tif")):
                tif_stk = read_tif_stack(os.path.join(chandir, f"{chan}_stk.tif"))
                tif_stk_avg = np.mean(tif_stk, axis=0)
                # Write the averaged image to a new .tif file         
                tifffile.imwrite(os.path.join(chandir, f"{chan}_stk_avg.tif"), tif_stk_avg.astype(np.uint16))
                print("Average tif-file is made from stack")
                
            if not os.path.isfile(os.path.join(chandir, f"{chan}_stk_avg.jpg")):
                tif_stk = read_tif_stack(os.path.join(chandir, f"{chan}_stk.tif"))
                tif_stk_avg = np.mean(tif_stk, axis=0)
                # Save the array as a JPEG image
                imageio.imwrite(os.path.join(chandir, f"{chan}_stk_avg.jpg"), tif_stk_avg.astype(np.uint8))
            
            # Where are the jupyter files for making the next steps??
            # Should they get uploaded to Github as well?
            
            ## Step 3: Calculate the SNR and FT-SNR and save as a .txt file?
            # step 3a: Check if file is written
            # parent_path = os.path.dirname(os.path.dirname(__file__))
            print(f"Root: {root}")
            if not os.path.isfile(os.path.join(root,"DATA",chan,"stats.txt")):
                print("generating stats...")
                # read the .tif stack
                imagedir = os.path.join(chandir, f"{chan}_stk_avg.tif")
                print(f"image directory: {imagedir}")
                tif_stk_avg = read_tif_stack(imagedir)
                tif_stk_avg_flat = tif_stk_avg.flatten()
                snr_ft = calculate_snr_frequency_domain(tif_stk_avg)
                snr_basic = calculate_simple_snr(tif_stk_avg)
                # write it in the text-file
                with open(os.path.join(root,"DATA",chan,"stats.txt"), 'w') as file:
                    file.write(f'SNR_basic = {snr_basic}\n')
                    file.write(f'SNR_FT = {snr_ft}\n')
            if os.path.isfile(os.path.join(root,"stats.txt")):
                with open(os.path.join(root,"stats.txt"), 'r') as file:
                  for line in file:
                    if "basic" in line:
                      # Assuming the parameter value is immediately after the '=' sign
                      SNR = line.split('=')[1].strip()
                      print(f"SNR = {SNR}")
                    if "FT" in line:
                      FTSNR = line.split('=')[1].strip()
                      print(f"FTSNR = {FTSNR}")

            ## Step 4: Create .png file from the .tif file using tif2png
            tif_file = os.path.join(root, "DATA", chan, f"{chan}_stk_avg.tif")
            png_file = os.path.join(root, "DATA", chan, f"{chan}_stk_avg.png")
            if os.path.isfile(tif_file):
                print(f"Yes, tiffile exists: {tif_file}")
                if os.path.isfile(png_file):
                    print(f"{png_file} already exists. Skipped...")
                else:
                    print(f"Creating .png file from {tif_file}")
                    tif2png(tif_file, png_file)

                      
                
                
            
            
                
                
                
                
                
                
                
                