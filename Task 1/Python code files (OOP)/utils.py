import os
import shutil
from math import radians, sin, cos, sqrt, atan2

# I keep constants in one place so other files can reuse them.
DB_NAME = "unieats.db"
IMAGE_FOLDER = "review_images"


try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None
    ImageTk = None

try:
    import tkintermapview
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False
    tkintermapview = None


class DistanceCalculator:
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # This is the standard formula to calculate distance on earth.
        earth_radius = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius * c


class ShellSort:
    # Self-study algorithm: Shell Sort
    @staticmethod
    def sort(item_list, key_function, reverse=False):
        arr = item_list[:]
        n = len(arr)
        gap = n // 2

        while gap > 0:
            i = gap
            while i < n:
                temp = arr[i]
                j = i

                if reverse is False:
                    while j >= gap and key_function(arr[j - gap]) > key_function(temp):
                        arr[j] = arr[j - gap]
                        j = j - gap
                else:
                    while j >= gap and key_function(arr[j - gap]) < key_function(temp):
                        arr[j] = arr[j - gap]
                        j = j - gap

                arr[j] = temp
                i = i + 1

            gap = gap // 2

        return arr


def ensure_image_folder():
    # Create the folder if it does not exist.
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)


def save_review_image(source_path):
    # Copy selected image into our project folder.
    if source_path == "":
        return ""
    if not os.path.exists(source_path):
        return ""

    ensure_image_folder()

    original_name = os.path.basename(source_path)
    base_name, ext_name = os.path.splitext(original_name)
    destination_path = os.path.join(IMAGE_FOLDER, original_name)
    counter = 1

    # Prevent file overwrite.
    while os.path.exists(destination_path):
        new_name = base_name + "_" + str(counter) + ext_name
        destination_path = os.path.join(IMAGE_FOLDER, new_name)
        counter = counter + 1

    shutil.copy(source_path, destination_path)
    return destination_path
