import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from Main import Bias  # Importing Bias from Main.py
from matplotlib import colors
import os

def process_bias(bias_files, show_plot=True, save_path=None):
    master_bias = np.mean(bias_files, axis=0)

    if show_plot:
        plt.imshow(master_bias, cmap='hot', origin='lower', norm=colors.LogNorm(vmin=np.percentile(master_bias, 5), vmax=np.percentile(master_bias, 95)))
        plt.colorbar(format='%.2f')
        plt.title("Master Bias Frame")
        plt.show()

    # Save the master bias
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True) # Ensure the folder exists
        hdu = fits.PrimaryHDU(master_bias)
        hdu.writeto(save_path, overwrite=True)
        print(f"Master bias frame saved to {save_path}")
    
    return master_bias

save_folder = 'G:/MyProject/TGP/data_reduction/Master_Bias'
save_filename = 'master_bias.fits'
save_path = os.path.join(save_folder, save_filename)

master_bias = process_bias(Bias, show_plot=True, save_path=save_path)
