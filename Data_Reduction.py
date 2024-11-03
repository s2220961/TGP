import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os
import gc
from matplotlib import colors
from Main import m52, ngc7789, Standard_Star_1, Standard_Star_2  # Importing data from Main.py

bias_master_dir = 'G:/MyProject/TGP/data_reduction/Master_Bias'
master_flats_dir = 'G:/MyProject/TGP/data_reduction/Flats/Master'
reduced_image_dir = 'G:/MyProject/TGP/data_reduction/Reduced Image'  # Directory where the processed (reduced) FITS files will be saved

if not os.path.exists(reduced_image_dir):
    os.makedirs(reduced_image_dir)

def load_master_bias():
    master_bias_path = os.path.join(bias_master_dir, 'Master_Bias.fits')
    if os.path.exists(master_bias_path):
        with fits.open(master_bias_path) as hdul:
            master_bias = hdul[0].data
            return master_bias
    else:
        print("Master bias file not found.")
        return None

master_bias = load_master_bias()
if master_bias is None:
    raise FileNotFoundError("Master bias file could not be loaded. Please ensure it exists in the specified directory.")

def load_master_flat(band):
    master_flat_path = os.path.join(master_flats_dir, f'Master_Flat_{band}.fits')
    if os.path.exists(master_flat_path):
        with fits.open(master_flat_path) as hdul:
            master_flat = hdul[0].data
            return master_flat
    else:
        print(f"Master flat file for {band} not found.")
        return None

# load the master flats into the dictionary for each available type from our image
master_flats = {}
filter_types = ['B-Band', 'U-Band', 'V-Band']
for filter_type in filter_types:
    master_flat = load_master_flat(filter_type)
    if master_flat is not None:
        master_flats[filter_type] = master_flat

def subtract_bias(fits_data, master_bias):
    master_bias = master_bias.astype(np.float32)  # Convert to float32 to reduce memory usage
    result = [lights_data.astype(np.float32) - master_bias for lights_data in fits_data]
    gc.collect()  # Force garbage collection to free memory
    return result
    
def divide_flat(fits_data, master_flat):
    master_flat = master_flat.astype(np.float32)
    result = [lights_data.astype(np.float32) / master_flat for lights_data in fits_data]
    gc.collect()
    return result

#dictionary to store the imported FITS data from Main.py
fits_data = {
    'M52': m52,
    'NGC7789': ngc7789,
    'Standard Star 1': Standard_Star_1,
    'Standard Star 2': Standard_Star_2
}

# subtract master bias and divide by its respective master flat for each band and object
for obj_name in ['M52', 'NGC7789', 'Standard Star 1', 'Standard Star 2']:
    for band in ['B-band', 'U-band', 'V-band']:
        # Check if FITS data exists for the current band
        if band in fits_data[obj_name] and fits_data[obj_name][band]:
            # Subtract master bias
            fits_data[obj_name][band] = subtract_bias(fits_data[obj_name][band], master_bias)

            # Map the correct master flat for each band
            flat_bands_map = {
                'B-band': 'B-Band',
                'U-band': 'U-Band',
                'V-band': 'V-Band'
            }

            if flat_bands_map[band] in master_flats:
                fits_data[obj_name][band] = divide_flat(fits_data[obj_name][band], master_flats[flat_bands_map[band]])
                print(f"Divided {obj_name} {band} by {flat_bands_map[band]} master flat.")
            else:
                print(f"Master flat {flat_bands_map[band]} not found for {band}, skipping flat-field correction.")

            # Save the processed data to the reduced image directory
            for i, data in enumerate(fits_data[obj_name][band]):
                reduced_image_filename = f"Reduced_Image_{obj_name}_{band.replace('-', '_')}_{i+1}.fits"
                obj_band_dir = os.path.join(reduced_image_dir, obj_name, band)
                if not os.path.exists(obj_band_dir):
                    os.makedirs(obj_band_dir)
                reduced_image_path = os.path.join(obj_band_dir, reduced_image_filename)

                # write the reduced data to a FITS file
                hdu = fits.PrimaryHDU(data)
                hdu.writeto(reduced_image_path, overwrite=True)
                print(f"Saved reduced image for {obj_name} {band} as {reduced_image_filename} in {obj_band_dir}.")

print("Image reduction complete.")
