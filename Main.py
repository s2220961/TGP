#Read Fits files

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import matplotlib.patches as mpatches
import scipy as scipy
import os

# Have a look at README.MD before replacing the base_dir to make sure your folder has the same structure. This code is built for only that kind of structure
# This gives the directory to your data folder. Please replace it with your own folder directory
base_dir = 'G:\MyProject\TGP\observation_data'


fits_data = {
    'Calibration': {},
    'M52': {'B-band': [], 'U-band': [], 'V-band': []},
    'NGC7789': {'B-band': [], 'U-band': [], 'V-band': []},
    'Standard Star 1': {'B-band': [], 'U-band': [], 'V-band': []},
    'Standard Star 2': {'B-band': [], 'U-band': [], 'V-band': []}
}

# Function to read FITS files from a given directory and add data to a list
def load_fits_files(directory):
    fits_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.fits'):
            file_path = os.path.join(directory, file_name)
            data = fits.getdata(file_path)
            fits_files.append(data)
    return fits_files

# Load Calibration data for Bias, Dark, and Flats
for cal_type in ['Bias', 'Dark', 'Flats']:
    dir_path = os.path.join(base_dir, 'Calibration', cal_type)

    if cal_type == 'Flats':
        flats_subfolders = ['B-Band', 'Halpha', 'OIII', 'R-Band', 'SII', 'V-Band']
        fits_data['Calibration']['Flats'] = {}  
        for subfolder in flats_subfolders:
            subfolder_path = os.path.join(dir_path, subfolder)
            fits_data['Calibration']['Flats'][subfolder] = load_fits_files(subfolder_path)
    else:
        fits_data['Calibration'][cal_type] = load_fits_files(dir_path)

# Load data for M52, NGC7789
for obj_name in ['M52', 'NGC7789']:
    for band in ['B-band', 'U-band', 'V-band']:
        dir_path = os.path.join(base_dir, obj_name, band)
        fits_data[obj_name][band] = load_fits_files(dir_path)

# Load data for Standard Star 1 and 2
for star in ['Standard Star 1', 'Standard Star 2']:
    for band in ['B-band', 'U-band', 'V-band']:
        fits_data[star][band] = []
        for observation in ['First observation', 'Second observation', 'Third observation']:
            dir_path = os.path.join(base_dir, star, band, observation)
            fits_data[star][band].extend(load_fits_files(dir_path))



# Example on how to fetch the data . In this example, I want to fecth the first data in V-band for M52 and Flats B-Band
# m52_b_band_data = fits_data['M52']['B-band']
# print(m52_b_band_data)

# flats_b_band_data = fits_data['Calibration']['Flats']['B-Band'][5]
# print(flats_b_band_data)
