import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from matplotlib import ticker

# Import fits_data from Main.py
from Main import fits_data

# Function to read FITS files from a given directory and add data to a list
def load_fits_files(directory):
    fits_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.fits'):
            file_path = os.path.join(directory, file_name)
            data = fits.getdata(file_path)
            fits_files.append(data)
    return fits_files

# Function to normalize a flat field frame
def normalize_flat(flat_data):
    mean_value = np.mean(flat_data)
    if mean_value == 0:
        print("Warning: Mean value of flat data is 0, normalization skipped.")
        return flat_data  # Return unnormalized data
    normalized_flat = flat_data / mean_value
    return normalized_flat

# Function to process and stack flat frames from a list of file paths and save master flats
def process_flats_and_save(flat_files, output_file):
    normalized_flats = []
    for flat_data in flat_files:
        print(f"Processing flat data.")
        normalized_flat = normalize_flat(flat_data)
        normalized_flats.append(normalized_flat)
    
    if not normalized_flats:
        print("No valid flats were processed.")
        return None

    master_flat = np.median(normalized_flats, axis=0)
    
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory {output_dir}: {e}")
            return

    try:
        hdu = fits.PrimaryHDU(master_flat)
        hdu.writeto(output_file, overwrite=True)
        print(f"Master flat saved to: {output_file}")
    except Exception as e:
        print(f"Error saving file {output_file}: {e}")

    return master_flat  # Return the master flat for plotting

# Function to plot the master flat with enhanced contrast and color scaling
def plot_master_flat(master_flat, title):
    if master_flat is not None:
        plt.imshow(master_flat, cmap='hot', origin='lower',
                   norm=colors.LogNorm(vmin=np.percentile(master_flat, 5), vmax=np.percentile(master_flat, 95)))
        plt.colorbar(format='%.2f')
        plt.title(title)
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        plt.gca().ticklabel_format(style='plain', axis='both')
        plt.show()
    else:
        print(f"No master flat to plot for {title}")

# Process and save master flats for each filter
output_base_dir = 'G:\\MyProject\\TGP\\data_reduction\\Flats\\Master'
for filter_name, flat_data in fits_data['Calibration']['Flats'].items():
    output_path = os.path.join(output_base_dir, f'Master_Flat_{filter_name}.fits')
    master_flat = process_flats_and_save(flat_data, output_path)
    plot_master_flat(master_flat, f'Master Flat for {filter_name} Band')

# Add debug prints to verify paths
# print("\nVerifying file paths:")
# for filter_name, flat_data in fits_data['Calibration']['Flats'].items():
#     print(f"\nChecking {filter_name} filter files:")
#     for data in flat_data:
#         print(f"Data exists with shape: {data.shape}")





# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# from astropy.io import fits
# from matplotlib import ticker

# # Function to normalize a flat field frame
# def normalize_flat(flat_data):
#     mean_value = np.mean(flat_data)
#     if mean_value == 0:
#         print("Warning: Mean value of flat data is 0, normalization skipped.")
#         return flat_data  # Return unnormalized data
#     normalized_flat = flat_data / mean_value
#     return normalized_flat

# # Function to process and stack flat frames from a list of file paths and save master flats
# def process_flats_and_save(flat_files, output_file):
#     normalized_flats = []
#     for file_path in flat_files:
#         if os.path.exists(file_path):
#             print(f"Processing file: {file_path}")
#             with fits.open(file_path) as hdul:
#                 flat_data = hdul[0].data  # Assuming the image data is in the primary HDU
#                 normalized_flat = normalize_flat(flat_data)
#                 normalized_flats.append(normalized_flat)
#         else:
#             print(f"File does NOT exist: {file_path}, skipping.")
    
#     # Stack the normalized flats (using median stacking to reduce noise)
#     if not normalized_flats:
#         print("No valid flats were processed.")
#         return None

#     master_flat = np.median(normalized_flats, axis=0)
    
#     # Create output directory if it does not exist
#     output_dir = os.path.dirname(output_file)
#     if not os.path.exists(output_dir):
#         try:
#             os.makedirs(output_dir)
#             print(f"Created directory: {output_dir}")
#         except OSError as e:
#             print(f"Error creating directory {output_dir}: {e}")
#             return

#     # Save the master flat to a FITS file
#     try:
#         hdu = fits.PrimaryHDU(master_flat)
#         hdu.writeto(output_file, overwrite=True)
#         print(f"Master flat saved to: {output_file}")
#     except Exception as e:
#         print(f"Error saving file {output_file}: {e}")

#     return master_flat  # Return the master flat for plotting

# # Function to plot the master flat with enhanced contrast and color scaling
# def plot_master_flat(master_flat, title):
#     if master_flat is not None:
#         plt.imshow(master_flat, cmap='hot', origin='lower',
#                    norm=colors.LogNorm(vmin=np.percentile(master_flat, 5), vmax=np.percentile(master_flat, 95)))
#         plt.colorbar(format='%.2f')
#         plt.title(title)
#         plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
#         plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
#         plt.gca().ticklabel_format(style='plain', axis='both')
#         plt.show()
#     else:
#         print(f"No master flat to plot for {title}")

# # List of flat field FITS files for each filter with corrected paths
# flat_files_dict = {
#     'B': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91064_flats_B_00_2024_09_27_06_43_25.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91063_flats_B_01_2024_09_27_06_42_58.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91060_flats_B_04_2024_09_27_06_41_28.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91061_flats_B_03_2024_09_27_06_41_59.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91059_flats_B_05_2024_09_27_06_41_03.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B-Band\PIRATE_91062_flats_B_02_2024_09_27_06_42_29.fits'
#     ],
    
#     'V': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\V-Band\PIRATE_91057_flats_V_03_2024_09_27_06_39_39.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\V-Band\PIRATE_91058_flats_V_02_2024_09_27_06_40_16.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\V-Band\PIRATE_91055_flats_V_05_2024_09_27_06_38_38.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\V-Band\PIRATE_91056_flats_V_04_2024_09_27_06_39_02.fits'
#     ],

#     'Halpha': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\Halpha\PIRATE_91067_flats_Halpha_01_2024_09_27_06_45_17.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\Halpha\PIRATE_91068_flats_Halpha_00_2024_09_27_06_46_07.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\Halpha\PIRATE_91065_flats_Halpha_03_2024_09_27_06_44_17.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\Halpha\PIRATE_91066_flats_Halpha_02_2024_09_27_06_44_43.fits'
#     ],

#     'OIII': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\OIII\PIRATE_91075_flats_OIII_01_2024_09_27_06_49_51.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\OIII\PIRATE_91076_flats_OIII_00_2024_09_27_06_50_29.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\OIII\PIRATE_91073_flats_OIII_03_2024_09_27_06_49_03.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\OIII\PIRATE_91074_flats_OIII_02_2024_09_27_06_49_23.fits'
#     ],

#     'R': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91049_flats_R_05_2024_09_27_06_34_00.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91054_flats_R_00_2024_09_27_06_37_40.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91052_flats_R_02_2024_09_27_06_36_02.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91053_flats_R_01_2024_09_27_06_36_52.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91050_flats_R_04_2024_09_27_06_34_24.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R-Band\PIRATE_91051_flats_R_03_2024_09_27_06_35_13.fits'
#     ],

#     'SII': [
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\SII\PIRATE_91070_flats_SII_02_2024_09_27_06_47_22.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\SII\PIRATE_91071_flats_SII_01_2024_09_27_06_47_50.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\SII\PIRATE_91069_flats_SII_03_2024_09_27_06_47_01.fits',
#         r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\SII\PIRATE_91072_flats_SII_00_2024_09_27_06_48_25.fits'
#     ]
# }

# # Process and save master flats for each filter
# for filter_name, file_list in flat_files_dict.items():
#     output_path = rf'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\data reduction\Flats\Master\Master_Flat_{filter_name}.fits'
#     master_flat = process_flats_and_save(file_list, output_path)
#     plot_master_flat(master_flat, f"Master Flat for {filter_name} Band")

# # Add debug prints to verify paths
# print("\nVerifying file paths:")
# for filter_name, file_list in flat_files_dict.items():
#     print(f"\nChecking {filter_name} filter files:")
#     for file_path in file_list:
#         print(f"Checking if file exists: {file_path}")
#         print(f"File exists: {os.path.exists(file_path)}")
