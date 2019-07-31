import pysftp
import os
from ioservice.uploaders.Uploader import Uploader
from utils.Utils import cfg, current_time_in_millis, time_taken, is_empty, is_empty_arr
import configs.ConfigConstant as Cc
import utils.Constants as Sc
from ioservice.HostConfig import HostConfig
from auditlogging.Auditor import audit_params

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


class MoveFilesOnRemote(Uploader):
    """
    Move files from one remote directory to another

    """

    def __init__(self, files: list):
        """
        Initiates the required SFTP configurations from 'config.yaml'
        file to prepare for file move

        1. Host
        2. Port
        3. Username
        4. Secret (password or SSH private key path) > this implementation auto detects whether
            to connect using password or private key file
        5. Remote source directory path
        6. Remote destination directory path

        Parameters
        ----------
        files : list
                a list of files to be moveed on remote host

        """
        self._files = files
        self._srcDir = cfg(Cc.SOURCE_DIRECTORY)
        self._sftpHost = cfg(Cc.SOURCE_HOST)
        self._sftpPort = cfg(Cc.SOURCE_PORT)
        self._sftpUsername = cfg(Cc.SOURCE_USERNAME)
        self._sftpSecret = cfg(Cc.SOURCE_SECRET)
        self._destDir = cfg(Cc.ARCHIVE_DIRECTORY)

    def fromconfig(self, configs: HostConfig):
        self._srcDir = configs.getsrc()
        self._sftpHost = configs.gethost()
        self._sftpPort = configs.getport()
        self._sftpUsername = configs.getuser()
        self._sftpSecret = configs.getsecret()
        self._destDir = configs.getdest()

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
        Overrides a list of files to be used to perform files move operations on remote host.
        It is usefull when user just wants to pass a new list of files.

        Parameters
        ----------
        files
            a new list of files

        """
        if not is_empty_arr(files):
            self._files = files

    def upload(self) -> list:
        """
        Connects to SFTP host and transfers files from a remote source to destination directory

        Returns
        -------
        list
            a list of files transferred

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

            for file in self._files:
                _src = os.path.join(self._srcDir, os.path.basename(file))
                _dest = os.path.join(self._destDir, os.path.basename(file))
                _start = current_time_in_millis()
                file_comments = '({}) ==> ({}) transfer'.format(_src, _dest)

                audit_params(operation=Sc.OPERATION_FILE_TRANSFER,
                             status=Sc.STATUS_PROCESSING,
                             comments=file_comments + 'ing...')

                _sftp.rename(_src, _dest)

                audit_params(operation=Sc.OPERATION_FILE_TRANSFER,
                             status=Sc.STATUS_COMPLETE,
                             comments=file_comments + 'ed' + time_taken(_start))

        finally:
            if _sftp is not None:
                _sftp.close()

        return self._files


# fl = ['Text-1.txt']
# o = MoveFilesOnRemote(fl)
# o.change_dir(src='/files/from/', dest='/files/to/')
# o.upload()
