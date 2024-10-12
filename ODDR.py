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


# Directory where the master flats are stored
master_flats_dir = 'G:\\MyProject\\TGP\\data_reduction\\Flats\\Master'

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
filter_types = ['B-Band', 'Halpha', 'OIII', 'R-Band', 'SII', 'V-Band']
for filter_type in filter_types:
    master_flat = load_master_flat(filter_type)
    if master_flat is not None:
        master_flats[filter_type] = master_flat

# Function to subtract master bias from FITS data
def subtract_bias(fits_data, master_bias):
    master_bias = master_bias.astype(np.float32)  # Convert to float32 to reduce memory usage
    result = [lights_data.astype(np.float32) - master_bias for lights_data in fits_data]
    gc.collect()  # Force garbage collection to free memory
    return result

# Function to divide FITS data by a master flat
def divide_flat(fits_data, master_flat):
    master_flat = master_flat.astype(np.float32)
    result = [lights_data.astype(np.float32) / master_flat for lights_data in fits_data]
    gc.collect()
    return result

# Subtract master bias and divide by all master flats for each band and object
for obj_name in ['M52', 'NGC7789', 'Standard Star 1', 'Standard Star 2']:
    for band in ['B-band', 'U-band', 'V-band']:  l
        fits_data[obj_name][band] = subtract_bias(fits_data[obj_name][band], master_bias)  # Subtract master bias
        flat_bands_map = {                                                                 # Divide 
            'B-band': 'B-Band',
            'U-band': 'U-band', 
            'V-band': 'V-Band'
        }
        
        for flat_band_key in flat_bands_map:
            if flat_bands_map[flat_band_key] in master_flats:  # Ensure master flat exists
                fits_data[obj_name][band] = divide_flat(fits_data[obj_name][band], master_flats[flat_bands_map[flat_band_key]])
                print(f"Divided {obj_name} {band} by {flat_bands_map[flat_band_key]} master flat.")
            else:
                print(f"Master flat {flat_bands_map[flat_band_key]} not found, skipping flat-field correction.")

# print(fits_data['M52']['V-band'][0])

# Function to plot reduced FITS data with a colorbar
def plot_reduced_data_with_colorbar(reduced_data, title):
    if reduced_data is not None and len(reduced_data) > 0:
        median_image = np.median(reduced_data, axis=0) # We take the median image of the reduced data list
        plt.figure(figsize=(10, 8))
        plt.imshow(median_image, cmap='viridis', origin='lower',
                   norm=colors.LogNorm(vmin=np.percentile(median_image, 5), vmax=np.percentile(median_image, 95)))
        
        plt.colorbar(label='Pixel Value')
        plt.title(title)
        plt.xlabel('X Pixel')
        plt.ylabel('Y Pixel')
        plt.show()
    else:
        print(f"No valid data to plot for {title}")


plot_reduced_data_with_colorbar(fits_data['M52']['B-band'], 'M52 B-band Reduced Data') #Second variable is the title
