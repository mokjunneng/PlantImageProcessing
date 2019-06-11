# PlantImageProcessing

Processing pipeline and workflow:
1. Extract plant images from Amazon S3 and store in `./tmp` directory.
2. Process `tmp` images using custom range thresholding and some cv2 functions where processed images (plants' binary mask) will be stored in `./output-images` directory.
3. Results information
    a. Pixel surface area data is stored in `surface_area_results.txt`
    b. Color channel histogram data is stored in `./color-bins` as `.npy` files. It is a dictionary of numpy array histogram values for each channel. E.g. `{'r': [100, 2, ... 320], 'g': [42, 32, ..., 22], 'b':[69, 23, ..., 0]}`

# Instructions to run
`python main.py [-s --stereo] [-d --startdate '$Y-%m-%d'] [-t --thread_count int]`
### Command-line arguments:
`-s --stereo`        If specified, images from both cameras will be returned for stereo image reconstruction.  
`-d --startdate`     If specified, images since the input start date will be retrieved. Else, the default start date will be a week before from current date  
`-t --thread_count`  Specify the number of worker threads to process the images.  

# Note
Make sure aws is configured with the right access and secret keys to access S3 storage
