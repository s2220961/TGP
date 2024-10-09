import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Function to process and stack bias frames from a list of file paths
def process_bias(bias_files):
    bias_frames = []
    for file_path in bias_files:
        print(f"Processing file: {file_path}")
        with fits.open(file_path) as hdul:
            bias_data = hdul[0].data  # Assuming the image data is in the primary HDU
            bias_frames.append(bias_data)
    # Stack the bias frames (using median stacking to reduce noise)
    master_bias = np.median(bias_frames, axis=0)
    return master_bias

# List of bias frame FITS files (placeholders for file paths)
bias_files = [
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90721_Bias11_0_2024_09_26_18_18_47.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90732_Bias11_1_2024_09_26_18_29_35.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90733_Bias11_2_2024_09_26_18_29_40.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90734_Bias11_3_2024_09_26_18_29_46.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90735_Bias11_4_2024_09_26_18_29_51.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90736_Bias11_5_2024_09_26_18_29_56.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90737_Bias11_6_2024_09_26_18_30_01.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90738_Bias11_7_2024_09_26_18_30_07.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90739_Bias11_8_2024_09_26_18_30_12.fits',
    r'C:\Users\fraze\Downloads\Data_Reduction\Bias\PIRATE_90740_Bias11_9_2024_09_26_18_30_17.fits'
]

# Process the bias frames
print("Processing bias frames...")
master_bias = process_bias(bias_files)

# Plot the master bias frame
plt.imshow(master_bias, cmap='hot', origin='lower')
plt.colorbar(format='%.2f')  # Format the color bar with floating point values
plt.title("Master Bias Frame")
plt.show()

print("Script execution complete.")