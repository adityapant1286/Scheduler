import pysftp
import os
from utils.Utils import cfg, current_time_in_millis, time_taken
import configs.ConfigConstant as Cc
import utils.Constants as Sc
from utils.Utils import is_empty, is_empty_arr
from ioservice.HostConfig import HostConfig
from ioservice.downloaders.Downloader import Downloader
from auditlogging.Auditor import audit_params

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


class RemoteDownloader(Downloader):
    """
    Provides implementation for downloading files from a remote host using SFTP.

    """

    def __init__(self):
        """
        Retrieves required SFTP configurations from configurations

        1. Host
        2. Port
        3. Username
        4. Secret (password or SSH private key path) > this implementation auto detects whether
            to connect using password or private key file
        5. Remote location source directory path
        6. localhost destination directory path
        7. File extensions to be filter

        """
        self._srcDir = cfg(Cc.SOURCE_DIRECTORY)
        self._sftpHost = cfg(Cc.SOURCE_HOST)
        self._sftpPort = cfg(Cc.SOURCE_PORT)
        self._sftpUsername = cfg(Cc.SOURCE_USERNAME)
        self._sftpSecret = cfg(Cc.SOURCE_SECRET)
        self._destDir = cfg(Cc.TARGET_DIRECTORY)
        self._file_ext = cfg(Cc.FILE_EXTENSIONS)

    def fromconfig(self, configs: HostConfig):
        """
        Allows to change configurations at runtime

        Parameters
        ----------
        configs : HostConfig
                  Custom configurations which will be used for SFTP connection

        """
        self._srcDir = configs.getsrc()
        self._sftpHost = configs.gethost()
        self._sftpPort = configs.getport()
        self._sftpUsername = configs.getuser()
        self._sftpSecret = configs.getsecret()
        self._destDir = configs.getdest()
        self._file_ext = configs.getfile_ext()

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

    def change_files(self, files: list = None):
        """
        Not require for this operation.

        Parameters
        ----------
        files
            NA

        """
        raise NotImplementedError

    def download(self) -> list:
        """
        Connects to SFTP host using configurations
        and scans for files as per the extensions mentioned in the configurations.
        If there are any matching files, they will be downloaded to destination
        with total seconds taken to download files.

        Returns
        --------
        list
            a list of downloaded files ordered by modified time in ascending.
            Earliest will be the first.

        """
        _sftp = None
        try:
            if self._sftpSecret.find(os.sep) == -1:
                _sftp = pysftp.Connection(self._sftpHost,
                                          username=self._sftpUsername,
                                          password=self._sftpSecret,
                                          port=self._sftpPort,
                                          cnopts=cnopts)
            else:
                _sftp = pysftp.Connection(self._sftpHost,
                                          username=self._sftpUsername,
                                          private_key=self._sftpSecret,
                                          port=self._sftpPort,
                                          cnopts=cnopts)
            _sftp.chdir(self._srcDir)

            _start = current_time_in_millis()

            # audit_params(operation=Sc.OPERATION_DOWNLOAD,
            #              status=Sc.STATUS_PROCESSING,
            #              comments=Sc.MSG_FILES_DOWNLOADING)

            self._download_them(_sftp)

            # audit_params(operation=Sc.OPERATION_DOWNLOAD,
            #              status=Sc.STATUS_COMPLETE,
            #              comments=Sc.MSG_FILES_DOWNLOADED + time_taken(_start))
        finally:
            if _sftp is not None:
                _sftp.close()

        return self._downloaded_files()

    def _download_them(self, _sftp: pysftp.Connection):
        """
        This method does the hard work downloading files. It also preserves the modified time
        after downloaded from the SFTP host.
        The call back lambda function prints the % byes downloaded,
        which is based on the size of the file.

        Parameters
        ----------
        _sftp : pysftp.Connection
                a sftp connection object

        """
        entries = _sftp.listdir(self._srcDir)

        for entry in entries:
            if _sftp.isfile(entry) and self._is_file_asked(entry):

                _sftp.get(os.path.join(self._srcDir, entry),
                          os.path.join(self._destDir, entry),
                          callback=lambda transfered, size: audit_params(operation=Sc.OPERATION_DOWNLOAD,
                                                                         status=Sc.STATUS_COMPLETE,
                                                                         comments="{} {} ({})%".format('>>-->', entry, str("%.2f" % (100*(int(transfered)/int(size)))))),
                          preserve_mtime=True)

    def _downloaded_files(self) -> list:
        """
        Scans the local downloaded directory and sorts the files based on modified time.
        Earliest will be the first and latest will be at the end of collection.

        Returns
        --------
        list
            sorted list of downloaded files in the destination directory

        """
        _files = []
        with os.scandir(self._destDir) as it:
            for entry in it:
                if self._isfile(entry) and self._is_file_asked(entry.name):
                    _files.append(entry)

        if len(_files) > 0:
            _files.sort(key=lambda f: f.stat().st_mtime)
            _sorted = list(map(lambda f: os.path.join(self._destDir, f.name), _files))
            return _sorted
        else:
            return _files

    @staticmethod
    def _isfile(entry):
        return not entry.name.startswith('.') and not entry.name.startswith('__init__') and entry.is_file()

    def _is_file_asked(self, fname):
        _ext = fname[fname.rfind('.') + 1:]
        return _ext in self._file_ext


# rd = RemoteDownloader()
# rd.download()