from ioservice.uploaders.Uploader import Uploader
from utils.Utils import cfg, current_time_in_millis, time_taken, is_empty, is_empty_arr
import configs.ConfigConstant as Cc
import utils.Constants as Sc
from auditlogging.Auditor import audit_params
import os
import shutil


class LocalUploader(Uploader):
    """
    Provide implementation for Uploader abstract class.
    This implementation copy files from one directory to another on localhost

    """

    def __init__(self, files: list, move: bool = False):
        """
        Accepts a list of files for upload operation and copy to destination directory.

        1. Localhost destination directory path
        2. A list of file extensions to be used to filter files

        Parameters
        ----------
        files : list
                a list of files to be uploaded

        move : bool
                If true files will be moved to destination, copy otherwise

        """
        self._srcDir = cfg(Cc.TARGET_DIRECTORY)
        self._destDir = cfg(Cc.OUTPUT_DIRECTORY)
        self._file_ext = cfg(Cc.FILE_EXTENSIONS)
        self._move = move
        self._files = files

    def change_dir(self, src: str = None, dest: str = None):
        """
        Overrides the source / destination directory path

        Parameters
        ----------
        src : str
                source directory path
        dest : str
                destination directory path

        """
        if not is_empty(src):
            self._srcDir = src

        if not is_empty(dest):
            self._destDir = dest

    def change_files(self, files: list = None):
        """
        Override files to be uploade.

        Parameters
        ----------
        files : list
                a new list of files

        Returns
        -------

        """
        if not is_empty_arr(files):
            self._files = files

    def change_file_ext(self, file_ext: list = None):
        """
        Override file extensions for filter.

        Parameters
        ----------
        file_ext : list
                    a list of file extensions to be filterred

        """
        if not is_empty_arr(file_ext):
            self._file_ext = file_ext

    def set_move(self, move: bool = False):
        """
        Set this flag to true if you need to peform move operation

        Parameters
        ----------
        move : bool
                overrides default move flag.
                If true files will be moved to destination, copy otherwise

        """
        self._move = move

    def upload(self) -> list:
        """
        Copy or move files to destination

        Returns
        --------
        list
            a list of files transferred to destination

        """
        _done = []
        for entry in self._files:
            if self._isfile(entry) and self._is_file_asked(entry):
                dest_path = os.path.join(self._destDir, os.path.basename(entry))
                src_path = os.path.join(self._srcDir, os.path.basename(entry))
                file_comments = '({}) ==> ({}) transfer'.format(src_path, dest_path)
                _start = current_time_in_millis()

                audit_params(operation=Sc.OPERATION_UPLOAD,
                             status=Sc.STATUS_PROCESSING,
                             comments=file_comments + 'ing...')

                if self._move:
                    shutil.move(src=src_path, dst=dest_path)
                else:
                    shutil.copy2(src_path, dest_path)

                audit_params(operation=Sc.OPERATION_UPLOAD,
                             status=Sc.STATUS_COMPLETE,
                             comments=file_comments + 'ed' + time_taken(_start))

                _done.append(dest_path)

        return _done

    @staticmethod
    def _isfile(entry: str) -> bool:
        return not entry.startswith('.') and not entry.startswith('__init__') and entry.rfind('.') > -1

    def _is_file_asked(self, fname):
        ext = fname[fname.rfind('.') + 1:]
        return ext in self._file_ext


# fl = ['C:/Users/jsubramaniam/Documents/Box Sync/Box Sync/Dont hear just listen/input/Zuora_DM_Orders_Example_jagan_successes_only.csv', 'Zuora_DM_Orders_Example_jagan_successes_only.csv']
# lu = LocalUploader(files=fl)
# lu.change_dir(src='C:/Users/jsubramaniam/Documents/Box Sync/Box Sync/Dont hear just listen/input/',
#               dest='C:/Users/jsubramaniam/Documents/Box Sync/Box Sync/Dont hear just listen/error/')
# lu.change_file_ext(file_ext=['csv'])
# lu.upload()
