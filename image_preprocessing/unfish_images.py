import os
import sys
import cv2
import numpy as np
from zipper import Zipper


class UnfishImages:

    def __init__(self, extracted_path: str):

        # Paths to temporary extracted files
        self.extracted_path = extracted_path
        self.images_path = os.path.join(self.extracted_path,
                                        'recording_car_tub')

        # Define camera matrix K
        self.K = np.array([[673.9683892, 0., 343.68638231],
                           [0., 676.08466459, 245.31865398],
                           [0., 0., 1.]])

        # Define distortion coefficients d
        self.d = np.array([-0.36824145, 0.2848545, 0.00079123,
                      0.00064924, -0.16345661])

    def unfish_image(self, img: np.array) -> np.array:

        # Read an example image and acquire its size
        h, w = img.shape[:2]

        # Generate new camera matrix from parameters
        newcameramatrix, roi = cv2.getOptimalNewCameraMatrix(self.K,
                                                             self.d,
                                                             (w,h), 0)

        # Generate look-up tables for remapping the camera image
        mapx, mapy = cv2.initUndistortRectifyMap(self.K, self.d, None,
                                                 newcameramatrix,
                                                 (w, h), 5)

        # Remap the original image to a new image
        new_img = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        return new_img

    def transform_images(self):
        """ Map unfish to all extracted images """

        for filename in os.listdir(self.images_path):
            # Unfish only jpgs
            if filename.endswith('.jpg'):
                file_path = os.path.join(self.images_path,
                                         filename)

                img = cv2.imread(file_path)

                # Can unfish only unempty images
                if(type(img) is np.ndarray):
                    new_img = self.unfish_image(img)
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
    unfish = UnfishImages(extracted_path)
    zipper = Zipper(archive_path, extracted_path)
    zipper.unzip_images()
    unfish.transform_images()
    zipper.zip_back(new_archive_name)
