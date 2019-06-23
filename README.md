# PlantImageProcessing

Processing pipeline and workflow:
1. Extract plant images from Amazon S3 and store in `./tmp` directory.
2. Process `tmp` images using custom range thresholding and some cv2 functions where processed images (plants' binary mask) will be stored in `./output-images` directory.
3. Results information
  * Pixel surface area data is stored in `surface_area_results.txt`
  * If stereo=False, growth information will be calculated from the surface area results where result will be stored in `growth.npy`
  * Color channel histogram data is stored in `./color-bins` as `.npy` files. It is a dictionary of numpy array histogram values for each channel. E.g. `{'r': [100, 2, ... 320], 'g': [42, 32, ..., 22], 'b':[69, 23, ..., 0]}`

# Instructions to run
`python main.py [-s --stereo] [-d --startdate '$Y-%m-%d-%H'] [-e --enddate '$Y-%m-%d-%H'] [-t --thread_count int]`
### Command-line arguments:
`-s --stereo`        If specified, images from both cameras will be returned for stereo image reconstruction.  
`-d --startdate`     Filter images since this date time  (required)  
`-e --enddate`       Filter images till this date time  (required)  
`-t --thread_count`  Specify the number of worker threads to process the images.  

# Note
Make sure aws is configured with the right access and secret keys to access S3 storage
