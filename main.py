import argparse
from datetime import datetime
import os
import shutil

import numpy as np
import cv2
from scipy.ndimage.filters import median_filter

from s3helper import get_images_key, download_images
from image_processing import hsv_custom_range_threshold, rgb_custom_range_threshold, pseudo_surface_area, color_analysis, undistort_image

TEMP_IMAGE_STORAGE_DIR = "tmp"
PROCESSED_IMAGE_DIR = "output-images"
COLOR_BINS_DIR = "color-bins"
IMAGE_STORAGE_DIR = "stored"


# Parse command-line arguments (not used for now)
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    # parser.add_argument("-i", "--image", help="Input image file.", required=True)
    # parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    # parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False, action="store_true")
    # parser.add_argument("-D", "--debug", help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.", default=None)
    args = parser.parse_args()
    return args

# args = options()

def run_image_processing_workflow(image):
    tmp_img = os.path.join(TEMP_IMAGE_STORAGE_DIR, image)
    img = cv2.imread(tmp_img)

    # Obtain plant mask
    hsv_lower_thresh = [25, 35, 35]
    hsv_upper_thresh = [60, 255, 255]

    rgb_lower_thresh = [0, 100, 0]
    rgb_upper_thresh = [200, 255, 200]

    hsv_mask, hsv_masked_img = hsv_custom_range_threshold(img, hsv_lower_thresh, hsv_upper_thresh)
    rgb_mask, rgb_masked_img = rgb_custom_range_threshold(img, rgb_lower_thresh, rgb_upper_thresh)

    combined_mask = cv2.bitwise_and(hsv_mask, rgb_mask)
    denoised_mask = median_filter(combined_mask, size=12)

    # Obtain "surface area" information
    surface_area, area_percentage = pseudo_surface_area(denoised_mask)

    # Obtain color channels histogram bins
    histogram_bins = color_analysis(img, denoised_mask)

    # Write results
    outfile = os.path.join(PROCESSED_IMAGE_DIR, image.split(".")[0] + "_mask.png")
    print(f"Writing image file {outfile}")
    cv2.imwrite(outfile, denoised_mask)
    with open("surface_area_results.txt", "a") as f:
        f.write(f"{outfile} - {surface_area} {area_percentage} \n")
    np.save(os.path.join(COLOR_BINS_DIR, image.split(".")[0] + "_colorbins.npy"), histogram_bins)

    # Move tmp image file to stored dir
    stored_img = os.path.join(IMAGE_STORAGE_DIR, image)
    if not os.path.exists(stored_img):
        shutil.move(tmp_img, stored_img)
    else:
        os.remove(tmp_img)

# Main Worflow
def main():
    # Create directories if not exist
    if not os.path.exists(PROCESSED_IMAGE_DIR):
        os.makedirs(PROCESSED_IMAGE_DIR)
    if not os.path.exists(COLOR_BINS_DIR):
        os.makedirs(COLOR_BINS_DIR)
    if not os.path.exists(IMAGE_STORAGE_DIR):
        os.makedirs(IMAGE_STORAGE_DIR)

    # Download images from S3
    start_date = datetime(2019, 6, 1)
    image_keys = get_images_key(start_date=start_date.timestamp())
    download_images(image_keys)

    # Run image processing workflow
    for image in os.listdir(TEMP_IMAGE_STORAGE_DIR):
        undistort_image(os.path.join(TEMP_IMAGE_STORAGE_DIR, image))
        run_image_processing_workflow(image)


if __name__ == "__main__":
    main()
