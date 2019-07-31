from ioservice.cleaners.Cleaner import Cleaner
from utils.Utils import is_empty
import os
import shutil


class DirectoryCleaner(Cleaner):
    """
    Provides a directory cleanup implementation

    """

    def __init__(self, src: str, remove_subdirs: bool = False):
        """
        Accepts a directory path to be clean and additional parameter
        to indicate whether to clean sub directories as well

        Parameters
        ----------
        src : str
                  a directory path to be cleaned
        remove_subdirs : bool
                        if true sub-directories will be cleaned,
                        else only files contain in directory path

        """
        self._src_dir = src
        self._remove_subdirs = remove_subdirs

    def clean(self):
        """
        Lists all entries in the directory path, then deletes each file from
        underlying file system.
        If remove_subdirs it True, then files inside sub directories will be deleted too.

        Raises
        -------
        Exception
            an Exception in case of file system issues

        """
        for entry in os.listdir(self._src_dir):
            file_path = os.path.join(self._src_dir, entry)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif self._remove_subdirs and os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as ex:
                raise ex

    def change_dir(self, src: str = None, dest: str = None):
        """
        Overrides the source directory path to be clean.
        Destination directory will be ignored.

        Parameters
        ----------
        src : str
                source directory path
        dest : str
                not required to be passed

        """
        if not is_empty(src):
            self._src_dir = src

    def change_files(self, files: list = None):
        """
        Not required for this operation

        Parameters
        ----------
        files
            NA

        """
        raise NotImplementedError

