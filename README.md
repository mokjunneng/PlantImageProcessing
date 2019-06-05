# PlantImageProcessing

Processing pipeline and workflow:
1. Extract plant images from Amazon S3 and store in `./tmp` directory.
2. Process `tmp` images using custom range thresholding and some cv2 functions where processed images (plants' binary mask) will be stored in `./output-images` directory.
3. Results information such as pixel surface area and color channel decomposition are written as `.txt` and `.npy` format

# Instructions to run
`python main.py`

# Note
Make sure aws is configured with the right access and secret keys to access S3 storage
