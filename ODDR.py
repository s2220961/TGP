# Updated Python script for modifying file paths to OneDrive paths

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.visualization import SqrtStretch, ImageNormalize
import os

class DataReductionPipeline:
    def __init__(self):
        self.master_bias = None
        self.master_flats = {}
        self.reduced_frames = []
        
    def load_master_bias(self, bias_file):
        """Load the master bias frame"""
        print(f"Loading master bias from: {bias_file}")
        with fits.open(bias_file) as hdul:
            self.master_bias = hdul[0].data
            
    def load_master_flats(self, flat_files_dict):
        """Load master flat frames for each filter"""
        for filter_name, flat_file in flat_files_dict.items():
            print(f"Loading master flat for {filter_name} filter from: {flat_file}")
            with fits.open(flat_file) as hdul:
                flat_data = hdul[0].data
                # Normalize the flat
                self.master_flats[filter_name] = flat_data / np.mean(flat_data)
                
    def reduce_science_frame(self, science_file, filter_name):
        """Reduce a single science frame"""
        if self.master_bias is None:
            raise ValueError("Master bias frame not loaded")
        if filter_name not in self.master_flats:
            raise ValueError(f"No master flat loaded for filter {filter_name}")
            
        with fits.open(science_file) as hdul:
            # Get exposure time for normalization
            exptime = float(hdul[0].header.get('EXPTIME', 1.0))
            
            # Perform reduction steps
            raw_data = hdul[0].data
            bias_subtracted = raw_data - self.master_bias
            flat_fielded = bias_subtracted / self.master_flats[filter_name]
            
            # Normalize to 1-second exposure
            normalized = flat_fielded / exptime
            
            return normalized
            
    def process_science_frames(self, science_files_dict):
        """Process all science frames by filter"""
        reduced_frames_dict = {}
        
        for filter_name, files in science_files_dict.items():
            print(f"\nProcessing {filter_name} filter science frames...")
            reduced_frames = []
            
            for file in files:
                print(f"Reducing: {os.path.basename(file)}")
                reduced = self.reduce_science_frame(file, filter_name)
                reduced_frames.append(reduced)
            
            # Stack the frames using median combining
            if reduced_frames:
                stacked_frame = np.median(reduced_frames, axis=0)
                reduced_frames_dict[filter_name] = stacked_frame
                
        return reduced_frames_dict
    
    def plot_reduced_frame(self, frame, title):
        """Plot a reduced frame with improved visualization"""
        norm = ImageNormalize(frame, stretch=SqrtStretch())
        
        plt.figure(figsize=(10, 8))
        plt.imshow(frame, origin='lower', norm=norm, cmap='viridis')
        plt.colorbar(label='Counts/second')
        plt.title(title)
        plt.show()

# Function to create a dictionary of file paths from a directory
def get_file_dict(directory):
    file_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.fits'):
            file_dict[filename] = os.path.join(directory, filename)
    return file_dict

# Example usage
if __name__ == "__main__":
    # Initialize the pipeline
    pipeline = DataReductionPipeline()
    
    # Load master bias
    master_bias_file = r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Bias\PIRATE_90721_Bias11_0_2024_09_26_18_18_47.fits'
    pipeline.load_master_bias(master_bias_file)
    
    # Define master flat files for each filter
    master_flat_files = {
        'B': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\B_Flat\Master_Flat_B.fits',
        'V': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\V_Flat\Master_Flat_V.fits',
        'R': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\R_Flat\Master_Flat_R.fits',
        'Halpha': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\Halpha_Flat\Master_Flat_Halpha.fits',
        'OIII': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\OIII_Flat\Master_Flat_OIII.fits',
        'SII': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\Calibration\Flats\SII_Flat\Master_Flat_SII.fits'
    }
    
    pipeline.load_master_flats(master_flat_files)
    
    # Define directories for science frames for each filter
    science_directories = {
        'B': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\M52\B_Band',
        'V': r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\observation data\M52\V_Band'
    }

    # Create a dictionary of science files for each filter
    science_files = {filter_name: list(get_file_dict(directory).values()) 
                     for filter_name, directory in science_directories.items()}
    
    # Process all science frames
    reduced_frames = pipeline.process_science_frames(science_files)
    
    # Plot reduced and stacked frames for each filter
    for filter_name, reduced_frame in reduced_frames.items():
        pipeline.plot_reduced_frame(
            reduced_frame, 
            f"Reduced and Stacked Science Frame - {filter_name} Filter"
        )

# Updated script for processing and stacking bias frames from a list of file paths

x