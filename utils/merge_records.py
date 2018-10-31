import sys
import os
from shutil import copyfile

def merge_two_dirs(dir_1: str, dir_2: str, dest: str) -> None:
    """
    Merge files from dir_1 and dir_2 to the destination
    avoiding filenames conflicts by new enumeration of
    files in dir_2
    """

    # Paths to dirs
    path_dir_1 = os.path.join(os.getcwd(), dir_1)
    path_dir_2 = os.path.join(os.getcwd(), dir_2)
    dest_path = os.path.join(os.getcwd(), dest)

    # Create destination directory
    try:
        os.mkdir(dest)
    except FileExistsError:
        print('Wrong destination')
        sys.exit()


    # Need to update indexes in names from dir_2
    index_shift = len(os.listdir(path_dir_1))

    # Copy files from dir_2 to dest and rename them
    for filename in os.listdir(path_dir_2):

        # File paths
        old_filename_path = os.path.join(path_dir_2, filename)
        new_filename_path = os.path.join(dest, filename)

        # Copy file to dest
        copyfile(old_filename_path, new_filename_path)

        if filename.endswith('.jpg'):
            # Rename .jpgs
            index = filename.split('_')[0]
            new_index = str(int(index) + index_shift)
            new_name = new_index + '_image_array_.jpg'
            os.rename(new_filename_path,
                      os.path.join(dest_path, new_name))
        elif filename.endswith('meta.json'):
            pass
        else:
            # Rename .jsons
            index = filename.split('_')[1][:-5]
            new_index = str(int(index) + index_shift)
            new_name = 'record_' + new_index + '.json'
            os.rename(new_filename_path,
                      os.path.join(dest_path, new_name))

    # Copy files from dir_1 to dest
    for filename in os.listdir(path_dir_1):

        # File paths
        old_filename_path = os.path.join(path_dir_1, filename)
        new_filename_path = os.path.join(dest, filename)

        # Copy file to dest
        copyfile(old_filename_path, new_filename_path)


if __name__ == "__main__":
    try:
        dir_1 = sys.argv[1]
        dir_2 = sys.argv[2]
        dest = sys.argv[3]

        merge_two_dirs(dir_1, dir_2, dest)
    except IndexError:
        print('Please pass two dirs')
