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
from PIL import Image
from matplotlib import pyplot as plt


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

    print(f"Image_shape = {image_shape}, and 'stack_tif_images' has been initiated...")

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

    # print(max_len)

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

    # print(np.shape(image_stack))

    # Write the stacked image to a new .tif file
    tifffile.imwrite(os.path.join(root, "Data", chan, f"{chan}_stk.tif"), image_stack)

def tif2png(tif_file, png_file):
    # Load the 16-bit TIFF image
    img = Image.open(tif_file)
    img_array = np.array(img)
    # Display the image with the desired colormap (replace 'coolwarm' with your choice)
    plt.imshow(img_array, cmap='coolwarm')
    # plt.draw()  # Force the figure to render (might be for Jupiter notebook only)
    # Get the image data
    # img_data = plt.gcf().canvas.tostring_rgb()

    plt.savefig(png_file)

    plt.close()

    ## Consider adding the rest of the editions if pdf-format doesn't work...

    # # Convert the image data to a PIL Image
    # width, height = plt.gcf().canvas.get_width_height()
    # img = Image.frombytes('RGB', (width, height), img_data)

    # # Normalize the image data to the 0-255 range (if necessary)
    # # img = img.point(lambda p: p * 255.0 / 65535.0)  # For 16-bit images

    # # Save the image as PNG
    # img.save(png_file)
    
    # print(f"{png_file} generated")