import os
import cv2
import numpy as np
import zipfile
import shutil


class UnfishImages:

    def __init__(self, archive_root_path: str, archive_name):

        # Define camera matrix K
        self.K = np.array([[673.9683892, 0., 343.68638231],
                           [0., 676.08466459, 245.31865398],
                           [0., 0., 1.]])

        # Define distortion coefficients d
        self.d = np.array([-0.36824145, 0.2848545, 0.00079123,
                      0.00064924, -0.16345661])

        # Paths
        self.archive_root_path = archive_root_path
        self.archive_path = os.path.join(self.archive_root_path,
                                         archive_name)
        self.temp_dir = os.path.join(self.archive_root_path,
                                     'Unzipped')



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

    def unzip_images(self):
        """ Unzip all files from arch to self.temp_dir """

        os.mkdir(self.temp_dir)

        with zipfile.ZipFile(self.archive_path) as archive:
            archive.extractall(self.temp_dir)

    def transform_images(self):
        """ Map unfish to all extracted images """

        temp_unzipped_path = os.path.join(self.temp_dir,
                                          'recording_car_tub')

        for filename in os.listdir(temp_unzipped_path):
            # Unfish only jpgs
            if filename.endswith('.jpg'):
                file_path = os.path.join('data'
                                         'recording_car_tub',
                                         filename)

                img = cv2.imread(file_path)

                # Can unfish only unempty images
                if(type(img) is np.ndarray):
                    new_img = self.unfish_image(img)
                    cv2.imwrite(file_path, new_img)

    def zip_back(self, new_archive_name: str) -> None:
        """ Create an archive of unfished images """

        new_archive_path = os.path.join(self.archive_root_path,
                                        new_archive_name)

        # Create new archive
        shutil.make_archive(new_archive_path, 'zip', self.temp_dir)

        # Remove temporary directory containing unfished images
        shutil.rmtree(self.temp_dir)

if __name__ == "__main__":

    # Path to data in the repo
    archive_root_path = os.path.join(os.getcwd(),
                                     'data')


    # Archive name (*.zip)
    archive_name = 'images.zip'

    # Do the stuff
    unfish = UnfishImages(archive_root_path, archive_name)
    unfish.unzip_images()
    unfish.transform_images()
    unfish.zip_back('new_images')
