import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from matplotlib import ticker
from Main import fits_data # Import fits_data from Main.py

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
def create_and_plot_master_flats():
    output_base_dir = 'G:\\MyProject\\TGP\\data_reduction\\Flats\\Master'
    for filter_name, flat_data in fits_data['Calibration']['Flats'].items():
        output_path = os.path.join(output_base_dir, f'Master_Flat_{filter_name}.fits')
        master_flat = process_flats_and_save(flat_data, output_path)
        plot_master_flat(master_flat, f'Master Flat for {filter_name} Band')

'''Please uncomment the code below to run the plot. I put a comment on the code below because Idont want it to run when I run the script'''
# create_and_plot_master_flats()

