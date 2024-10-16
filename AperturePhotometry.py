import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.visualization import SqrtStretch, ImageNormalize, ZScaleInterval
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from photutils.detection import DAOStarFinder
from astropy.convolution import Gaussian2DKernel, convolve
import os
from matplotlib.colors import LogNorm

# File paths for the reduced images
reduced_image_paths = [
    r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\data reduction\Reduced Images\Reduced_Stacked_Image_M52_B_band.fits',
    r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\data reduction\Reduced Images\Reduced_Stacked_Image_M52_U_band.fits',
    r'C:\Users\fraze\OneDrive - University of Edinburgh\Telescope Group Project\data reduction\Reduced Images\Reduced_Stacked_Image_M52_V_band.fits'
]

# Aperture Photometry for each file
for reduced_image_path in reduced_image_paths:
    if os.path.exists(reduced_image_path):
        with fits.open(reduced_image_path) as hdul:
            data = hdul[0].data

            # Apply Gaussian filter to smooth the image
            kernel = Gaussian2DKernel(x_stddev=1.5)
            data_smooth = convolve(data, kernel)

            # Estimate background noise statistics
            mean, median, std = sigma_clipped_stats(data_smooth, sigma=3.0)

            # Find stars using DAOStarFinder with adjusted parameters
            
            daofind = DAOStarFinder(fwhm=3.5, threshold=5.0*std, sharplo=0.4, sharphi=1.2, roundlo=-0.8, roundhi=0.8)

            sources = daofind(data_smooth - median)

            if sources is None or len(sources) == 0:
                print(f"No sources found in {reduced_image_path}")
                continue

            # Sort sources by flux and select top 500
            sources.sort('flux', reverse=True)
            sources = sources[:500]

            positions = np.transpose((sources['xcentroid'], sources['ycentroid']))

            # Define apertures with a consistent set of positions and variable radii
            fwhm = 3.0
            aperture_radius = 1.5 * fwhm
            aperture_sizes = sources['flux'] / np.max(sources['flux']) * aperture_radius  # Scale aperture size by flux
            apertures = CircularAperture(positions, r=aperture_radius)  # Use a fixed aperture for photometry
            scaled_apertures = [CircularAperture((x, y), r=r) for (x, y), r in zip(positions, aperture_sizes)]
            annulus_apertures = CircularAnnulus(positions, r_in=aperture_radius * 2, r_out=aperture_radius * 3)

            # Perform aperture photometry
            phot_table = aperture_photometry(data, apertures)
            bkg_table = aperture_photometry(data, annulus_apertures)

            # Compute sky-subtracted counts
            bkg_mean = bkg_table['aperture_sum'] / annulus_apertures.area
            phot_table['residual_aperture_sum'] = phot_table['aperture_sum'] - (bkg_mean * apertures.area)
            phot_table['instrumental_mag'] = -2.5 * np.log10(phot_table['residual_aperture_sum'])

            # Print photometry results
            print(f"Aperture photometry for {os.path.basename(reduced_image_path)}:")
            print(phot_table[['id', 'xcenter', 'ycenter', 'residual_aperture_sum', 'instrumental_mag']])

            # Visualize apertures
            plt.figure(figsize=(12, 10))
            
            # Use LogNorm for better contrast and 'hot' colormap for orange/red tones
            norm = LogNorm(vmin=np.percentile(data, 10), vmax=np.percentile(data, 99.9))
            plt.imshow(data, cmap='hot', origin='lower', norm=norm)
            
            # Plot scaled apertures with varying size and some transparency
            for aperture in scaled_apertures:
                aperture.plot(color='green', lw=1.5, alpha=0.3)
            annulus_apertures.plot(color='blue', lw=1.5, alpha=0.3)
            
            plt.colorbar(label='Flux (log scale)')
            plt.title(f"Aperture Photometry on {os.path.basename(reduced_image_path)}")
            plt.xlabel("X Pixel")
            plt.ylabel("Y Pixel")
            plt.show()