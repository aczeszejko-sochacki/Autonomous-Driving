import os
import zipfile
import shutil


class Zipper:

    def __init__(self, archive_path: str, extracted_path: str):
        self.archive_path = archive_path
        self.extracted_path = extracted_path

    def unzip_images(self) -> None:
        """
        Unzip all files from arch to cwd
        All extracted images will be placed
        in the tmp/recording_car_tub/
        """

        with zipfile.ZipFile(self.archive_path) as archive:
            archive.extractall(self.extracted_path)

    def zip_back(self, new_archive_name: str) -> None:
        """ Create an archive of images """

        # Required paths
        new_archive_path = os.path.join(os.getcwd(),
                                        'data',
                                        new_archive_name)

        # Create new archive
        shutil.make_archive(new_archive_path, 'zip',
                            self.extracted_path)

        # Remove temporary directory containing unfished images
        shutil.rmtree(self.extracted_path)
