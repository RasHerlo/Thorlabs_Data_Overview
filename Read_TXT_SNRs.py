# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 20:24:43 2024

@author: rasmu
"""

import os

data_path = os.path.dirname(os.path.dirname(__file__))

if not os.path.isfile(os.path.join(data_path,'SNR_FTSNR.txt')):
    print("file does not exist yet")
    

with open(os.path.join(data_path,'SNR_FTSNR.txt'), 'r') as file:
    content = file.read()
     
with open(os.path.join(data_path,'SNR_FTSNR.txt'), 'r') as file:
  for line in file:
    if "basic" in line:
      # Assuming the parameter value is immediately after the '=' sign
      SNR = line.split('=')[1].strip()
      print(f"SNR = {SNR}")
    if "FT" in line:
      FTSNR = line.split('=')[1].strip()
      print(f"FTSNR = {FTSNR}")
      
# return SNR, FTSNR