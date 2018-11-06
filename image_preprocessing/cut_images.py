import os
import sys
import numpy as np
import cv2
from zipper import Zipper


class CutImages:

    def __init__(self, extracted_path: str):

        # Paths to temporary extracted files
        self.extracted_path = extracted_path
        self.images_path = os.path.join(self.extracted_path,
                                        'recording_car_tub')

    def cut_image(self, img: np.array) -> np.array:
        """ The path is only at the bottom of the image """

        height = img.shape[0]
        new_img = img[2*height // 3 :]

        return new_img

    def cut_images(self):
        """ Map cutting to all extracted images """

        for filename in os.listdir(self.images_path):
            # Unfish only jpgs
            if filename.endswith('.jpg'):
                file_path = os.path.join(self.images_path,
                                         filename)

                img = cv2.imread(file_path)

                # Can unfish only unempty images
                if(type(img) is np.ndarray):
                    new_img = self.cut_image(img)
                    cv2.imwrite(file_path, new_img)


if __name__ == "__main__":
    try:
        archive_name = sys.argv[1]
        new_archive_name = sys.argv[2]
        archive_path = os.path.join(os.getcwd(), 'data', archive_name)

        if not os.path.isfile(archive_path):
            print('File does not exist')
            sys.exit()
    except IndexError:
        print('Please specify archive name')
        sys.exit()

    extracted_path = os.path.join(os.getcwd(), 'data', 'tmp')

    # Do the stuff
    cut = CutImages(extracted_path)
    zipper = Zipper(archive_path, extracted_path)
    zipper.unzip_images()
    cut.cut_images()
    zipper.zip_back(new_archive_name)
