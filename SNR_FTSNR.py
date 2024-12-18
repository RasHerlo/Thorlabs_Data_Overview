# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 20:03:35 2024

@author: rasmu
"""

import os

data_path = os.path.dirname(os.path.dirname(__file__))

print(f"Data_path = {data_path}")

with open(os.path.join(data_path,'SNR_FTSNR.txt'), 'w') as file:
    SNR = 5
    file.write(f'SNR_basic = {SNR}\n')
    FTSNR = 50
    file.write(f'SNR_FT = {FTSNR}\n')