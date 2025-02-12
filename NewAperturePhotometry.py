import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats, sigma_clip
from photutils.detection import DAOStarFinder
from photutils.psf import fit_fwhm
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
import os

# List of all reduced image paths.     
reduced_image_paths = [
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\M52\B-band\M52_normalized_Stacked_B-band.fits', 'M52_B'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\M52\U-band\M52_normalized_Stacked_U-band.fits', 'M52_U'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\M52\V-band\M52_normalized_Stacked_V-band.fits', 'M52_V'),

    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\NGC7789\B-band\NGC7789_normalized_Stacked_B-band.fits', 'NGC7789_B'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\NGC7789\U-band\NGC7789_normalized_Stacked_U-band.fits', 'NGC7789_U'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\NGC7789\V-band\NGC7789_normalized_Stacked_V-band.fits', 'NGC7789_V'),

    # Standard Star 1 - B-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\B-band\First Observation\SS1 normalized_Stacked_First Observation B.fits', 'Standard_Star_1_B_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\B-band\Second Observation\SS1 normalized_Stacked_Second Observation B.fits', 'Standard_Star_1_B_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\B-band\Third Observation\SS1 normalized_Stacked_Third Observation B.fits', 'Standard_Star_1_B_3rd'),

    # Standard Star 1 - U-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\U-band\First Observation\SS1 normalized_Stacked_First Observation U.fits', 'Standard_Star_1_U_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\U-band\Second Observation\SS1 normalized_Stacked_Second Observation U.fits', 'Standard_Star_1_U_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\U-band\Third Observation\SS1 normalized_Stacked_Third Observation U.fits', 'Standard_Star_1_U_3rd'),

    # Standard Star 1 - V-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\V-band\First Observation\SS1 normalized_Stacked_First Observation V.fits', 'Standard_Star_1_V_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\V-band\Second Observation\SS1 normalized_Stacked_Second Observation V.fits', 'Standard_Star_1_V_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 1\V-band\Third Observation\SS1 normalized_Stacked_Third Observation V.fits', 'Standard_Star_1_V_3rd'),

    # Standard Star 2 - B-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\B-band\First Observation\SS2 normalized_Stacked_First Observation B.fits', 'Standard_Star_2_B_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\B-band\Second Observation\SS2 normalized_Stacked_Second Observation B.fits', 'Standard_Star_2_B_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\B-band\Third Observation\SS2 normalized_Stacked_Third Observation B.fits', 'Standard_Star_2_B_3rd'),

    # Standard Star 2 - U-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\U-band\First Observation\SS2 normalized_Stacked_First Observation U.fits', 'Standard_Star_2_U_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\U-band\Second Observation\SS2 normalized_Stacked_Second Observation U.fits', 'Standard_Star_2_U_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\U-band\Third Observation\SS2 normalized_Stacked_Third Observation U.fits', 'Standard_Star_2_U_3rd'),

    # Standard Star 2 - V-band
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\V-band\First Observation\SS2 normalized_Stacked_First Observation V.fits', 'Standard_Star_2_V_1st'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\V-band\Second Observation\SS2 normalized_Stacked_Second Observation V.fits', 'Standard_Star_2_V_2nd'),
    (r'G:\MyProject\TGP\data_reduction\Normalized Aligned Stacked Images\Standard Star 2\V-band\Third Observation\SS2 normalized_Stacked_Third Observation V.fits', 'Standard_Star_2_V_3rd'),
]

# Dictionary to store results for each image
results = {}

# Loop through each reduced image path
for image_path, label in reduced_image_paths:
    print(f"Processing: {label}")

    # Ensure the file exists
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        continue

    with fits.open(image_path) as hdul:
        data = hdul[0].data.astype(np.float32)  # convert to float32 to save memory
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)

        # --- 1. First pass: initial FWHM guess ---
        initial_fwhm_guess = 3.0
        detection_threshold = 3.0 * std

        daofind_init = DAOStarFinder(fwhm=initial_fwhm_guess, threshold=detection_threshold)
        sources_init = daofind_init(data - median)

        if sources_init is None or len(sources_init) == 0:
            print(f"No sources found for {label} in first pass. Skipping.")
            continue

        # Filter out edge sources (example: 10-pixel border)
        mask = (
            (sources_init['xcentroid'] > 10) &
            (sources_init['xcentroid'] < data.shape[1] - 10) &
            (sources_init['ycentroid'] > 10) &
            (sources_init['ycentroid'] < data.shape[0] - 10)
        )
        sources_init = sources_init[mask]

        if len(sources_init) == 0:
            print(f"All detected sources were near edges for {label}, skipping.")
            continue

        # Sort initial sources by flux (descending)
        sources_init.sort('flux', reverse=True)

        # Limit the number of stars used for FWHM measurement (1st pass)
        n_fwhm_stars_first_pass = 100  # e.g. measure FWHM on the top 100 brightest
        top_sources_first_pass = sources_init[:n_fwhm_stars_first_pass]
        xypos_init = np.transpose((top_sources_first_pass['xcentroid'],
                                   top_sources_first_pass['ycentroid']))

        try:
            # Measure the FWHM from these top N stars
            fwhm_values_init = fit_fwhm(data, xypos=xypos_init, fit_shape=7)

            # Filter out non-converged fits
            good_mask = np.isfinite(fwhm_values_init) & (fwhm_values_init > 0)
            fwhm_values_init = fwhm_values_init[good_mask]

            if len(fwhm_values_init) == 0:
                print(f"No valid FWHM fits for {label} in the first pass.")
                continue

            fwhm_values_init_clipped = sigma_clip(fwhm_values_init, sigma=3.0, maxiters=5)
            median_fwhm_init = np.median(fwhm_values_init_clipped[~fwhm_values_init_clipped.mask])
            print(f"{label}: First-pass median FWHM = {median_fwhm_init:.2f} pixels")

            # --- 2. Second pass: use measured FWHM for detection ---
            daofind_refined = DAOStarFinder(fwhm=median_fwhm_init, threshold=detection_threshold)
            sources = daofind_refined(data - median)

            if sources is None or len(sources) == 0:
                print(f"No sources found for {label} in second pass. Skipping.")
                continue

            # Sort by flux again
            sources.sort('flux', reverse=True)

            # Limit the number of stars used for the second FWHM measurement
            n_fwhm_stars_second_pass = 100
            top_sources_second_pass = sources[:n_fwhm_stars_second_pass]
            xypos_2pass = np.transpose((top_sources_second_pass['xcentroid'],
                                        top_sources_second_pass['ycentroid']))

            # Dynamically compute fit_shape for the second pass
            fit_shape = int(round(1.5 * median_fwhm_init))
            if fit_shape < 7:
                fit_shape = 7
            if fit_shape % 2 == 0:
                fit_shape += 1

            fwhm_values = fit_fwhm(data, xypos=xypos_2pass, fit_shape=fit_shape)

            # Filter out invalid fits
            good_mask = np.isfinite(fwhm_values) & (fwhm_values > 0)
            fwhm_values = fwhm_values[good_mask]

            if len(fwhm_values) == 0:
                print(f"No valid FWHM fits for {label} in second pass.")
                continue

            fwhm_values_clipped = sigma_clip(fwhm_values, sigma=3.0, maxiters=5)
            median_fwhm_clipped = np.median(fwhm_values_clipped[~fwhm_values_clipped.mask])
            print(f"{label} - Clipped Median FWHM (2nd pass): {median_fwhm_clipped:.2f} pixels")

            # --- Aperture Photometry ---
            # We do photometry on ALL sources from the second pass, not just the top N
            xypos_all = np.transpose((sources['xcentroid'], sources['ycentroid']))

            aperture_radius = 3.0 * median_fwhm_clipped
            inner_radius = 2.0 * aperture_radius
            outer_radius = 3.0 * aperture_radius

            apertures = CircularAperture(xypos_all, r=aperture_radius)
            annulus_apertures = CircularAnnulus(xypos_all, r_in=inner_radius, r_out=outer_radius)

            n_sky = annulus_apertures.area
            n_pix = apertures.area
            if n_sky <= n_pix:
                print(f"Warning: Increase annulus size for {label} to ensure n_sky > n_pix.")

            phot_table = aperture_photometry(data, apertures)
            bkg_table = aperture_photometry(data, annulus_apertures)

            bkg_mean = bkg_table['aperture_sum'] / annulus_apertures.area
            phot_table['residual_aperture_sum'] = phot_table['aperture_sum'] - (bkg_mean * apertures.area)

            # Filter out non-positive flux
            positive_flux = phot_table['residual_aperture_sum'] > 0
            phot_table = phot_table[positive_flux]

            # Calculate instrumental magnitudes
            phot_table['instrumental_mag'] = -2.5 * np.log10(phot_table['residual_aperture_sum'])

            # NEW: Calculate SNR and magnitude errors
            # Calculate sky background variance in the annulus
            sky_variance = np.var(data[annulus_apertures.to_mask().get_overlap_slices(data)])
            
            # Calculate SNR for each source
            signal = phot_table['residual_aperture_sum']
            snr = signal / np.sqrt(signal + n_pix * sky_variance)
            
            # Calculate magnitude errors using dm = 1.086 * (1/SNR)
            phot_table['snr'] = snr
            phot_table['mag_error'] = 1.086 / snr

            # Store final results with new columns
            results[label] = phot_table[['id', 'xcenter', 'ycenter',
                                       'residual_aperture_sum', 'instrumental_mag',
                                       'snr', 'mag_error']]
            print(f"Photometry results for {label} stored.")

        except Exception as e:
            print(f"Error processing {label}: {e}")

# Display results
for label, result in results.items():
    print(f"\nResults for {label}:")
    print(result)

import pandas as pd

# Save each set of results to a CSV file
for label, photometry_data in results
