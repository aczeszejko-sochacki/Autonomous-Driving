import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from zipper import Zipper
from skimage.filters import sobel
from skimage.color import rgb2gray


class EdgeImages:

    def __init__(self, extracted_path: str):

        # Paths to temporary extracted files
        self.extracted_path = extracted_path
        self.images_path = os.path.join(self.extracted_path,
                                        'recording_car_tub')

    def edge_image(self, img: np.array) -> np.array:
        """
        Tranforms image to gray enabling finding
        contours
        """

        gray_img = rgb2gray(img)
        edge_img = sobel(gray_img)

        return edge_img

    def detect_edges(self):
        """ Map edge_image to all extracted images """

        for filename in os.listdir(self.images_path):
            # Unfish only jpgs
            if filename.endswith('.jpg'):
                file_path = os.path.join(self.images_path,
                                         filename)

                try:
                    img = plt.imread(file_path)
                except OSError:
                    # Unexpected error, probably caused by
                    # camera / connection problem 
                    pass

                # Can unfish only unempty images
                if(type(img) is np.ndarray):
                    new_img = self.edge_image(img)
                    plt.imsave(file_path, new_img)


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
    edge = EdgeImages(extracted_path)
    zipper = Zipper(archive_path, extracted_path)
    zipper.unzip_images()
    edge.detect_edges()
    zipper.zip_back(new_archive_name)
