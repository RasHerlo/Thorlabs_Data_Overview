# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:53:44 2024

@author: svw191
"""

import os
import shutil

# Prepare the test-folders:
    
rtdir = os.path.join(os.path.dirname(__file__),"LED +APs 240926")
chans = ["ChanA","ChanB"]

print(rtdir)

# Contains 3 experiments with 2 channels in each

## Cleaning: Removing the premade stacks, overview.pdf or averages

# In [240926_pl100_pc001_LED+APs500microW_ex01], only remove the png-files
# In [240926_pl100_pc001_LED+APs500microW_ex02], remove png + tif-avg
# In [240926_pl100_pc001_LED+APs500microW_ex01], remove png, tif-avg and tif-stk

import os


sub_1 = "240926_pl100_pc001_LED+APs500microW_ex01"
sub_2 = "240926_pl100_pc001_LED+APs500microW_ex02"
sub_3 = "240926_pl100_pc001_LED+APs500microW_ex03"

for chan in chans:
    png_file = os.path.join(rtdir,sub_1,"DATA",chan,f"{chan}_stk_avg.png")
    if os.path.isfile(png_file):
        os.remove(png_file)
    tif_file = os.path.join(rtdir,sub_2,"DATA",chan,f"{chan}_stk_avg.tif")
    if os.path.isfile(tif_file):
        os.remove(tif_file)
    if os.path.isdir(os.path.join(rtdir,sub_3,"DATA",chan)):
        print("removing folder")
        shutil.rmtree(os.path.join(rtdir,sub_3,"DATA",chan))




