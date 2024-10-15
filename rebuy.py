import os
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import ZScaleInterval

class ScienceFrameProcessor:
    def __init__(self, base_dir, master_bias_path, master_flats_dir):
        self.base_dir = base_dir
        self.master_bias_path = master_bias_path
        self.master_flats_dir = master_flats_dir
        self.filters = ['B', 'V', 'R', 'U', 'Halpha', 'OIII', 'SII']
        self.found_files = {filter_name: [] for filter_name in self.filters}
        
        # Load master bias at initialization
        try:
            with fits.open(self.master_bias_path) as hdul:
                self.master_bias = hdul[0].data
            print(f"Successfully loaded master bias from: {self.master_bias_path}")
        except Exception as e:
            print(f"Error loading master bias: {e}")
            self.master_bias = None

    def get_master_flat(self, filter_name):
        """Retrieve the master flat for a specific filter."""
        file_name = f"master_flat_{filter_name}.fits"
        file_path = os.path.join(self.master_flats_dir, file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Master flat file not found for filter {filter_name}")
        return file_path

    def reduce_science_frames(self, filter_name):
        """Reduce science frames by applying bias subtraction and flat fielding."""
        frame_list = self.found_files[filter_name]
        if not frame_list:
            print(f"No science frames found for filter {filter_name}")
            return None, None

        try:
            # First stack the raw science frames
            stacked_data = []
            for file_path in frame_list:
                with fits.open(file_path) as hdul:
                    data = hdul[0].data
                    if data is not None:
                        stacked_data.append(data)

            if not stacked_data:
                print(f"No valid data frames found for filter {filter_name}")
                return None, None

            # Stack frames by taking the median
            stacked_frame = np.median(stacked_data, axis=0)
            print(f"Stacked {len(stacked_data)} frames for filter {filter_name}")
            
            # Get the header from the first file
            with fits.open(frame_list[0]) as hdul:
                header = hdul[0].header

            # Apply bias subtraction
            if self.master_bias is None:
                raise ValueError("Master bias not loaded")
            bias_subtracted = stacked_frame - self.master_bias
            
            # Apply flat field correction
            with fits.open(self.get_master_flat(filter_name)) as flat_hdul:
                master_flat = flat_hdul[0].data
                
            # Normalize the master flat
            normalized_flat = master_flat / np.mean(master_flat)
            
            # Perform flat field correction
            reduced_frame = bias_subtracted / normalized_flat
            
            print(f"Successfully reduced frames for filter {filter_name}")
            return reduced_frame, header

        except Exception as e:
            print(f"Error reducing frames for filter {filter_name}: {e}")
            return None, None

    def plot_reduced_image(self, reduced_data, filter_name, output_dir):
        """Plot the final reduced science image with appropriate scaling for astronomical objects."""
        try:
            plt.figure(figsize=(12, 10))
            
            # Use ZScale for better visualization of astronomical features
            zscale = ZScaleInterval()
            vmin, vmax = zscale.get_limits(reduced_data)
            
            im = plt.imshow(reduced_data, cmap='gray', origin='lower', 
                          aspect='equal', vmin=vmin, vmax=vmax)
            
            plt.colorbar(im, label='Counts')
            plt.title(f'Reduced Science Image - {filter_name} Band')
            plt.xlabel('Pixel X')
            plt.ylabel('Pixel Y')
            
            # Save the plot
            plot_file = os.path.join(output_dir, f"Reduced_{filter_name}_science_image.png")
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.show()
            print(f"Saved reduced science image to: {plot_file}")
            
        except Exception as e:
            print(f"Error plotting reduced image for filter {filter_name}: {e}")

    def process_all_filters(self):
        """Process all filters and create reduced images."""
        print(f"\nSearching for science frames in directory: {self.base_dir}")
        
        try:
            # First, find all science frames
            for root, dirs, files in os.walk(self.base_dir):
                fits_files = [f for f in files if f.endswith('.fits')]
                if fits_files:
                    print(f"\nFound {len(fits_files)} FITS files in: {root}")
                
                for file in fits_files:
                    file_path = os.path.join(root, file)
                    try:
                        with fits.open(file_path) as hdul:
                            header = hdul[0].header
                            filter_name = self.get_filter_name(header)
                            if filter_name and self.is_science_frame(header):
                                self.found_files[filter_name].append(file_path)
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")

            # Create output directory
            output_dir = os.path.join(os.path.dirname(self.base_dir), 'Reduced_Images')
            os.makedirs(output_dir, exist_ok=True)

            # Process each filter
            for filter_name in self.filters:
                if self.found_files[filter_name]:
                    print(f"\nProcessing {filter_name} filter images...")
                    reduced_data, header = self.reduce_science_frames(filter_name)
                    
                    if reduced_data is not None:
                        # Save reduced data
                        output_file = os.path.join(output_dir, f"Reduced_{filter_name}_science_image.fits")
                        fits.writeto(output_file, reduced_data, header, overwrite=True)
                        print(f"Saved reduced data to: {output_file}")
                        
                        # Plot reduced image
                        self.plot_reduced_image(reduced_data, filter_name, output_dir)

        except Exception as e:
            print(f"Error during processing: {e}")

    def is_science_frame(self, header):
        """Check if the frame is a science frame."""
        frame_type = header.get('IMAGETYP', '').lower()
        object_name = header.get('OBJECT', '').lower()
        return object_name and not any(cal_type in frame_type for cal_type in ['bias', 'dark', 'flat'])

    def get_filter_name(self, header):
        """Get filter name from the FITS header."""
        filter_keywords = ['FILTER', 'FILT', 'FILTER1', 'FILTERNAME']
        filter_raw = None
        
        for keyword in filter_keywords:
            if keyword in header:
                filter_raw = str(header[keyword]).upper()
                break
        
        if not filter_raw:
            return None
        
        filter_map = {
            'B': ['B', 'BLUE', 'B-BAND'],
            'V': ['V', 'VISUAL', 'V-BAND'],
            'R': ['R', 'RED', 'R-BAND'],
            'U': ['U', 'ULTRAVIOLET', 'U-BAND'],
            'HALPHA': ['HALPHA', 'HA', 'H-ALPHA'],
            'OIII': ['OIII', 'O-III', 'O III', '[OIII]'],
            'SII': ['SII', 'S-II', 'S II', '[SII]']
        }
        
        for std_name, variations in filter_map.items():
            if any(var in filter_raw for var in variations):
                return std_name
                
        return None

def main():
    base_dir = r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\observation data\NGC7789'
    master_bias_path = r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\Calibration\master_bias.fits'
    master_flats_dir = r'C:\Users\finla\OneDrive - University of Edinburgh\Telescope Group Project\Calibration\MasterFlats'
    
    processor = ScienceFrameProcessor(base_dir, master_bias_path, master_flats_dir)
    processor.process_all_filters()

if __name__ == "__main__":
    main()
