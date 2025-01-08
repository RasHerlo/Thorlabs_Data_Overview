# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 20:24:43 2024

@author: rasmu
"""

# Input file ending with A_stk_avg.tif or B_stk_avg.tif from PDF_report_generator.py
# Output: SNR and FTSNR values

import os

# data_path = os.path.dirname(os.path.dirname(__file__))

def read_txt_snrs(filepath):
    
  data_path = os.path.dirname(filepath)

  print(f"Data_path = {data_path}")

  if not os.path.isfile(os.path.join(data_path,'stats.txt')):
      print("file does not exist yet")
      
  else:
    with open(os.path.join(data_path, 'stats.txt'), 'r') as file:
        content = file.read()
        
    with open(os.path.join(data_path,'stats.txt'), 'r') as file:
      for line in file:
        if "basic" in line:
          # Assuming the parameter value is immediately after the '=' sign
          SNR = line.split('=')[1].strip()
          print(f"SNR = {SNR}")
        if "FT" in line:
          FTSNR = line.split('=')[1].strip()
          print(f"FTSNR = {FTSNR}")
  return SNR, FTSNR