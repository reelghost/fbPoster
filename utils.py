# All the important functions for both
import os
import glob
import shutil


def get_first_image_path(folder_path='images'):
    image_extensions = ('*.png', '*.jpg', '*.jpeg')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
    image_files.sort()
    return os.path.abspath(image_files[0]) if image_files else None

def move_image_to_posted(image_path, destination_folder=os.getenv('POSTED_FOLDER', 'images_posted')):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.move(image_path, os.path.join(destination_folder, os.path.basename(image_path)))