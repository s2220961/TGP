''' The code works, but Im confused on how to handle the master flat. Since we have 6 kind of flats, 
how do I process them with the light data? (espescially since the light data is divided into 3 bands only) '''

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.visualization import SqrtStretch, ImageNormalize
import os
from Bias_Master import master_bias
from Main import fits_data  # Importing fits_data from Main.py
import gc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


master_flats_dir = 'G:\\MyProject\\TGP\\data_reduction\\Flats\\Master'

reduced_image_dir = 'G:\\MyProject\\TGP\\data_reduction\\Reduced Image'  # Directory where the processed (reduced) FITS files will be saved

# Create the directory for reduced image if it doesn't exist (We want to save the reduced images here)
if not os.path.exists(reduced_image_dir):
    os.makedirs(reduced_image_dir)


# Function to load the master flat for a given band from the directory
def load_master_flat(band):
    master_flat_path = os.path.join(master_flats_dir, f'Master_Flat_{band}.fits')
    if os.path.exists(master_flat_path):
        with fits.open(master_flat_path) as hdul:
            master_flat = hdul[0].data
            return master_flat
    else:
        print(f"Master flat file for {band} not found.")
        return None

master_flats = {}

# Load the master flats into the dictionary for each available type from your image
filter_types = ['B-Band', 'U-Band', 'V-Band']
for filter_type in filter_types:
    master_flat = load_master_flat(filter_type)
    if master_flat is not None:
        master_flats[filter_type] = master_flat

# Function to subtract master bias from FITS data
def subtract_bias(fits_data, master_bias):
    master_bias = master_bias.astype(np.float32)  # Convert to float32 to reduce memory usage, this is important for large data to prevent memory errors
    result = [lights_data.astype(np.float32) - master_bias for lights_data in fits_data]
    gc.collect()  # Force garbage collection to free memory, I recommend using this after large operations to free up memory
    return result

# Function to divide FITS data by a master flat
def divide_flat(fits_data, master_flat):
    master_flat = master_flat.astype(np.float32)
    result = [lights_data.astype(np.float32) / master_flat for lights_data in fits_data]
    gc.collect()
    return result

processed_data = {}

# Subtract master bias and divide by its respective master flat for each band and object
for obj_name in ['M52', 'NGC7789', 'Standard Star 1', 'Standard Star 2']:
    processed_data[obj_name] = {}  

    for band in ['B-band', 'U-band', 'V-band']:  
        processed_data[obj_name][band] = [] 

        fits_data[obj_name][band] = subtract_bias(fits_data[obj_name][band], master_bias)

        # This check if the correct flat is used for each band
        flat_bands_map = {                                                                 
            'B-band': 'B-Band',
            'U-band': 'U-Band',
            'V-band': 'V-Band'
        }

        # Check if the corresponding master flat for the current band exists
        if flat_bands_map[band] in master_flats: 
            fits_data[obj_name][band] = divide_flat(fits_data[obj_name][band], master_flats[flat_bands_map[band]])
            print(f"Divided {obj_name} {band} by {flat_bands_map[band]} master flat.")
        else:
            print(f"Master flat {flat_bands_map[band]} not found for {band}, skipping flat-field correction.")

        # Append the processed data into the list for stacking later
        processed_data[obj_name][band].extend(fits_data[obj_name][band])

# After processing all the data, calculate the mean and save the stacked image
for obj_name in processed_data:
    for band in processed_data[obj_name]:
        if len(processed_data[obj_name][band]) > 0:

            stacked_image = np.mean(processed_data[obj_name][band], axis=0)

            # Save the stacked image
            reduced_image_filename = f"Reduced_Stacked_Image_{obj_name}_{band.replace('-', '_')}.fits"
            reduced_image_path = os.path.join(reduced_image_dir, reduced_image_filename)
            
            # Save the stacked image to a FITS file
            hdu = fits.PrimaryHDU(stacked_image)
            hdu.writeto(reduced_image_path, overwrite=True)
            print(f"Saved reduced stacked image for {obj_name} {band} as {reduced_image_filename} in {reduced_image_dir}.")
        else:
            print(f"No valid data to stack for {obj_name} {band}, skipping saving.")
