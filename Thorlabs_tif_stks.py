# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:38:49 2024

@author: svw191
"""

# Sort the raw data and stack it

# input: raw datafiles (with bad numbering)
# output: saved .stk for each identified channel

# FUNCTIONS":
# read_tif_stack
import tifffile
# stack_tif_images
import os
import re
import numpy as np


def read_tif_stack(filename):
    """Reads a .tif image stack into a 3D NumPy array.

    Args:
        filename: The path to the .tif file.

    Returns:
        A 3D NumPy array containing the image stack.
    """

    with tifffile.TiffFile(filename) as tif:
        return tif.asarray()
    
def stack_tif_images(root, chan):

    # root = "C:\\Users\\svw191\\PythonFiles\\PythonTrial\\LED +APs 240926\\240926_pl100_pc001_LED+APs500microW_ex01\\"
    # chan = "ChanA"

    # Get a list of .tif files containing the search string
    tif_files = [f for f in os.listdir(root) if (f.endswith('.tif') or f.endswith('.ti')) and chan in f and 'Preview' not in f]

    first_image = tifffile.imread(os.path.join(root, tif_files[0]), key=0)  # Read the first page
    image_shape = first_image.shape

    print(image_shape)

    # # # Ensure consistent image format
    for file in tif_files:
        image = tifffile.imread(os.path.join(root, tif_files[0]), key=0)
        if image.shape != image_shape:
            print(f"Warning: Image format mismatch for {file}")
            # Implement conversion logic here (optional)

    # SOLVE PADDING ISSUE AND CHRONOLOGY FOR TIFS

    # Pad the smaller indices to match the longest one
    file_nums = []
    for file in tif_files:
        match = re.search(r"([^_\.]+)(\.[^.]+)$", file)
        file_num = match.group(1)
        file_nums.append(file_num)   

    longest_string = max(file_nums, key=len)
    max_len = len(longest_string)

    print(max_len)

    pad_files = []
    for file in tif_files:
        match = re.search(r"([^_\.]+)(\.[^.]+)$", file)
        file_num = match.group(1)
        file_num_pad = file_num.zfill(max_len)
        file = re.sub(rf"{re.escape(file_num)}\.", f"{file_num_pad}.", file)
        pad_files.append(file)

    indices = np.argsort(pad_files)

    sorted_files = []
    for i in range(len(indices)):
        sorted_files.append(tif_files[indices[i]])

    # Create an empty stack with correct data type
    image_stack = np.zeros((len(tif_files), *image_shape), dtype=first_image.dtype)

    # # # Iterate over the sorted files and add them to the stack
    for i, file in enumerate(tif_files):
        image = tifffile.imread(os.path.join(root,tif_files[indices[i]]), key=0)
        image_stack[i] = image

    print(np.shape(image_stack))

    # Write the stacked image to a new .tif file
    tifffile.imwrite(os.path.join(root, "Data", chan, f"{chan}_stk.tif"), image_stack)