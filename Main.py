#Read Fits files

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import matplotlib.patches as mpatches
import scipy as scipy
import os

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

# Load Calibration data
for cal_type in ['Bias', 'Dark', 'Flats']:
    dir_path = os.path.join(base_dir, 'Calibration', cal_type)
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



m52_v_band_data = fits_data['M52']['V-band'][0]
print(m52_v_band_data)
