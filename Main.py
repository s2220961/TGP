#Read Fits files

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os

# Have a look at README.MD before replacing the base_dir to make sure your folder has the same structure. This code is built for only that kind of structure
# This is the directory to your data folder. Replace it with your own folder directory
base_dir = 'G:\MyProject\TGP\observation_data'

# Function to remove the specified regions from the FITS data
def trim_fits_data(data):
    # Keep everything except the first region (rows 0:4096 and columns 4060:4096) 
    # We remove the columns 4060 to 4096 from the data (0 is the bottom, top is 4096)
    trimmed_data = np.delete(data, np.s_[4060:4097], axis=1)     # Remember that python slicing is exclusive of the end index as in this case 4096 is not included. axis=1 means we are removing columns and axis=0 means we are removing rows
    
    # removed the second region (rows 4076:4096 and columns 0:4096)
    # We remove the rows 4050 to 4096
    trimmed_data = np.delete(trimmed_data, np.s_[4050:4097], axis=0)

    # removed the third  region (rows 0:60and columns 0:4096)
    # We remove the rows 0 to 60
    trimmed_data = np.delete(trimmed_data, np.s_[0:60], axis=0)
    
    return trimmed_data

# Function to read, trim, and return modified FITS data
def load_and_trim_fits_files(directory):
    trimmed_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.fits'):
            file_path = os.path.join(directory, file_name)
            data = fits.getdata(file_path, memmap=False) 
            trimmed_data = trim_fits_data(data)  
            trimmed_files.append(trimmed_data)  
    return trimmed_files

Bias = []
Flats = {'B-Band': [], 'U-Band': [], 'V-Band': []}
M52 = {'B-band': [], 'U-band': [], 'V-band': []}
NGC7789 = {'B-band': [], 'U-band': [], 'V-band': []}
Standard_Star_1 = {'B-band': [], 'U-band': [], 'V-band': []}
Standard_Star_2 = {'B-band': [], 'U-band': [], 'V-band': []}

# Load and trim Bias data
bias_dir = os.path.join(base_dir, 'Calibration', 'Bias')
Bias = load_and_trim_fits_files(bias_dir)

# Load and trim Flats data for B-Band, U-Band, and V-Band
flats_dir = os.path.join(base_dir, 'Calibration', 'Flats')
for band in ['B-Band', 'U-Band', 'V-Band']:
    band_dir = os.path.join(flats_dir, band)
    Flats[band] = load_and_trim_fits_files(band_dir)

# Load and trim data for M52
for band in ['B-band', 'U-band', 'V-band']:
    dir_path = os.path.join(base_dir, 'M52', band)
    M52[band] = load_and_trim_fits_files(dir_path)

# Load and trim data for NGC7789
for band in ['B-band', 'U-band', 'V-band']:
    dir_path = os.path.join(base_dir, 'NGC7789', band)
    NGC7789[band] = load_and_trim_fits_files(dir_path)

# Load and trim data for Standard Star 1
for band in ['B-band', 'U-band', 'V-band']:
    Standard_Star_1[band] = []
    for observation in ['First observation', 'Second observation', 'Third observation']:
        dir_path = os.path.join(base_dir, 'Standard Star 1', band, observation)
        Standard_Star_1[band].extend(load_and_trim_fits_files(dir_path))

# Load and trim data for Standard Star 2
for band in ['B-band', 'U-band', 'V-band']:
    Standard_Star_2[band] = []
    for observation in ['First observation', 'Second observation', 'Third observation']:
        dir_path = os.path.join(base_dir, 'Standard Star 2', band, observation)
        Standard_Star_2[band].extend(load_and_trim_fits_files(dir_path))

# Example: on how to access and plot the data
# plt.imshow(Bias[0], cmap='viridis')
# plt.colorbar()
# plt.title("Trimmed Bias Data (after removing specified regions)")
# plt.show()
# print(Bias[0].shape)

# print(M52['B-band'][0])     # This will print the first data (array) of M52 in B-band














#Read Fits files

# import numpy as np
# import matplotlib.pyplot as plt
# from astropy.io import fits
# import os

# # Have a look at README.MD before replacing the base_dir to make sure your folder has the same structure. This code is built for only that kind of structure
# # This is the directory to your data folder. Replace it with your own folder directory
# base_dir = 'G:\MyProject\TGP\observation_data'

# # Function to remove the specified regions from the FITS data
# def trim_fits_data(data):
#     # Keep everything except the first region (rows 0:4096 and columns 4060:4096) 
#     # We remove the columns 4060 to 4096 from the data (0 is the bottom, top is 4096)
#     trimmed_data = np.delete(data, np.s_[4060:4097], axis=1)     # Remember that python slicing is exclusive of the end index as in this case 4096 is not included. axis=1 means we are removing columns and axis=0 means we are removing rows
    
#     # removed the second region (rows 4076:4096 and columns 0:4096)
#     # We remove the rows 4050 to 4096
#     trimmed_data = np.delete(trimmed_data, np.s_[4050:4097], axis=0)

#     # removed the third  region (rows 0:60and columns 0:4096)
#     # We remove the rows 0 to 60
#     trimmed_data = np.delete(trimmed_data, np.s_[0:60], axis=0)
    
#     return trimmed_data

# # Function to read, trim, and return modified FITS data
# def load_and_trim_fits_files(directory):
#     trimmed_files = []
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.fits'):
#             file_path = os.path.join(directory, file_name)
#             data = fits.getdata(file_path, memmap=False) 
#             trimmed_data = trim_fits_data(data)  
#             trimmed_files.append(trimmed_data)  
#     return trimmed_files

# Bias = []
# Flats = {'B-Band': [], 'U-Band': [], 'V-Band': []}
# m52 = {'B-band': [], 'U-band': [], 'V-band': []}
# ngc7789 = {'B-band': [], 'U-band': [], 'V-band': []}
# Standard_Star_1 = {'B-band': [], 'U-band': [], 'V-band': []}
# Standard_Star_2 = {'B-band': [], 'U-band': [], 'V-band': []}

# # Load and trim Bias data
# bias_dir = os.path.join(base_dir, 'Calibration', 'Bias')
# Bias = load_and_trim_fits_files(bias_dir)

# # Load and trim Flats data for B-Band, U-Band, and V-Band
# flats_dir = os.path.join(base_dir, 'Calibration', 'Flats')
# for band in ['B-Band', 'U-Band', 'V-Band']:
#     band_dir = os.path.join(flats_dir, band)
#     Flats[band] = load_and_trim_fits_files(band_dir)

# # Load and trim data for M52
# for band in ['B-band', 'U-band', 'V-band']:
#     dir_path = os.path.join(base_dir, 'M52', band)
#     m52[band] = load_and_trim_fits_files(dir_path)

# # Load and trim data for NGC7789
# for band in ['B-band', 'U-band', 'V-band']:
#     dir_path = os.path.join(base_dir, 'NGC7789', band)
#     ngc7789[band] = load_and_trim_fits_files(dir_path)

# # Load and trim data for Standard Star 1
# for band in ['B-band', 'U-band', 'V-band']:
#     dir_path = os.path.join(base_dir, 'Standard Star 1', band)
#     Standard_Star_1[band].extend(load_and_trim_fits_files(dir_path))

# # Load and trim data for Standard Star 2
# for band in ['B-band', 'U-band', 'V-band']:
#     dir_path = os.path.join(base_dir, 'Standard Star 2', band)
#     Standard_Star_2[band].extend(load_and_trim_fits_files(dir_path))
