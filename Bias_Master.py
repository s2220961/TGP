''' WORKS AS INTENDED '''
''' The script processes all of our Bias frame files, creates and then plots the Master '''

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from Main import Bias  # Importing Bias from Main.py
from matplotlib import colors


def process_bias(bias_files, show_plot=True):
    master_bias = np.median(bias_files, axis=0)
    if show_plot:
        plt.imshow(master_bias, cmap='hot', origin='lower' , norm=colors.LogNorm(vmin=np.percentile(master_bias, 5), vmax=np.percentile(master_bias, 95))) # Plot the master bias frame
        plt.colorbar(format='%.2f')
        plt.title("Master Bias Frame")
        plt.show()
    return master_bias

master_bias = process_bias(Bias, show_plot=False)  # Process the Bias frames and plot the master bias frame
