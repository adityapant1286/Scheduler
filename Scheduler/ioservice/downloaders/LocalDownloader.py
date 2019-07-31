import os
import shutil
from utils.Utils import cfg, current_time_in_millis, time_taken, is_empty
import utils.Constants as Sc
import configs.ConfigConstant as Cc
from ioservice.downloaders.Downloader import Downloader
from auditlogging.Auditor import audit_params


class LocalDownloader(Downloader):
    """
    This class provides implementation for localhost file copy operation
    from source to destination

    """

    def __init__(self):
        """
        Retrieve required file system paths from configurations

        1. Source directory path
        2. Destination directory path
        3. File extensions which will be used to filter out only required files

        """
        self._srcDir = cfg(Cc.SOURCE_DIRECTORY)
        self._destDir = cfg(Cc.TARGET_DIRECTORY)
        self._file_ext = cfg(Cc.FILE_EXTENSIONS)

    def change_dir(self, src: str = None, dest: str = None):
        """
        Overrides the source and/or destination directory

        Parameters
        ----------
        src : str
                source directory
        dest : str
                destination directory path

        """

        if not is_empty(src):
            self._srcDir = src

        if not is_empty(dest):
            self._destDir = dest

    def change_files(self, files: list = None):
        """
        Not required for this operation.

        Parameters
        ----------
        files
            NA

        """
        raise NotImplementedError

    def download(self) -> list:
        """
        Copy files from source directory to destination.
        Only files will be considered which are matches with the extension mentioned in the configurations.

        Returns
        --------
        list
            a list of copied files

        """
        files = []

        # scans source directory for files and filters out with extension and then copy
        with os.scandir(self._srcDir) as it:
            for entry in it:
                if self._isfile(entry) and self._is_file_asked(entry.name):
                    files.append(entry)
                    dest_path = os.path.join(self._destDir, entry.name)
                    file_comments = '({}) ==> ({}) transfer'.format(entry.path, dest_path)
                    _start = current_time_in_millis()
                    audit_params(operation=Sc.OPERATION_FILE_TRANSFER,
                                 status=Sc.STATUS_PROCESSING,
                                 comments=file_comments + 'ing...')

                    shutil.copy2(entry.path, dest_path)

                    audit_params(operation=Sc.OPERATION_FILE_TRANSFER,
                                 status=Sc.STATUS_COMPLETE,
                                 comments=file_comments + 'ed' + time_taken(_start))

        # sorts file entries by modified time. I
        # t is sorted by earliest modified time first and latest at the last
        if len(files) > 0:
            files.sort(key=lambda f: f.stat().st_mtime)
            print(files)
            return list(map(lambda f: os.path.join(self._destDir, f.name), files))
        else:
            return []

    @staticmethod
    def _isfile(entry):
        return not entry.name.startswith('.') and not entry.name.startswith('__init__') and entry.is_file()

    def _is_file_asked(self, fname):
        ext = fname[fname.rfind('.') + 1:]
        return ext in self._file_ext

