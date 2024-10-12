''' WORKS AS INTENDED '''
''' The script processes all of our Bias frame files, creates and then plots the Master '''

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from Main import fits_data  # Importing fits_data from Main.py

# Function to process and stack bias frames from a list of file paths
def process_bias(bias_files):

    # Stack the bias frames (using median stacking to reduce noise)
    master_bias = np.median(bias_files, axis=0)
    return master_bias

bias_files = fits_data['Calibration']['Bias']

master_bias = process_bias(bias_files)

# Plot the master bias frame
plt.imshow(master_bias, cmap='hot', origin='lower')
plt.colorbar(format='%.2f')  # Format the color bar with floating point values
plt.title("Master Bias Frame")
plt.show()

print("Script execution complete.")
