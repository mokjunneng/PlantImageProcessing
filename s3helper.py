import boto3
import logging
import os
from datetime import datetime


#TODO: Implement logging

BUCKET_NAME = "p3-images"
TEMP_IMAGE_STORAGE_DIRECTORY = "tmp"

s3 = boto3.client("s3")

def get_images_key(start_date=None, stereo=False):
    """
    Args:
        start_date: returns image keys beyond the date given here (float timestamp)
        stereo: if specified true, returns all keys, else returns only images captured by Camera 2
    Returns:
        List of image key names
    """
    format = "%Y-%m-%d-T%H:%M:%SZ"
    get_upload_time = lambda obj : int(datetime.strptime(obj['Key'].split('/')[-1].split('_')[0], format).timestamp())
    objs = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
    )['Contents']
    # Get reverse sorted s3 objects
    sorted_objs = [obj['Key'] for obj in sorted(objs, key=get_upload_time, reverse=True)]
    if not start_date:
        return sorted_objs
    truncated_objs = []
    get_camera_num = lambda obj : 2 if obj.find('2') != -1 else 1
    for obj in sorted_objs:
        new_obj = obj.split('/')[-1].split('_')
        upload_date = new_obj[0]
        camera_num = get_camera_num(new_obj[1])
        if datetime.strptime(upload_date, format).timestamp() >= start_date:
            if stereo:
                truncated_objs.append(obj)
            elif not stereo and camera_num == 1:
                truncated_objs.append(obj)
    return truncated_objs

def get_latest_image_key(stereo=False):
    return

def download_images(image_keys):
    if not os.path.exists(TEMP_IMAGE_STORAGE_DIRECTORY):
        os.makedirs(TEMP_IMAGE_STORAGE_DIRECTORY)
    for key in image_keys:
        _download_image(key)

def _download_image(key):
    filename = key.split('/')[-1]
    date = filename.split('_')[0]
    date = date.replace(':', '-')
    filename = date + filename.split('_')[1]
    filename = os.path.join(TEMP_IMAGE_STORAGE_DIRECTORY, filename)
    if not os.path.isfile(filename):
        print(f"Downloading {key} from S3...")
        with open(filename, 'wb') as f:
            s3.download_fileobj(BUCKET_NAME, key, f)
