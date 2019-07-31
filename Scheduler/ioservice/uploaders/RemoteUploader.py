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


class RemoteUploader(Uploader):
    """
    Provide implementation for Uploader abstract class.
    This implementation uploads files from localhost to a remote SFTP.

    """

    def __init__(self, files: list):
        """
        Accepts a list of files for upload operation and transfers to remote destination.
        Connection details retrieved from configurations.

        1. Host
        2. Port
        3. Username
        4. Secret (password or SSH private key path) > this implementation auto detects whether
            to connect using password or private key file
        5. Localhost source directory path
        6. Remote location destination directory path

        Parameters
        ----------
        files : a list of files to be uploaded

        """
        self._files = files
        self._srcDir = cfg(Cc.OUTPUT_DIRECTORY)
        self._sftpHost = cfg(Cc.SOURCE_HOST)
        self._sftpPort = cfg(Cc.SOURCE_PORT)
        self._sftpUsername = cfg(Cc.SOURCE_USERNAME)
        self._sftpSecret = cfg(Cc.SOURCE_SECRET)
        self._destDir = cfg(Cc.ARCHIVE_DIRECTORY)

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
        It is useful when user just wants to pass a new list of files.

        Parameters
        ----------
        files
            a new list of files

        """
        if not is_empty_arr(files):
            self._files = files

    def fromconfig(self, configs: HostConfig):
        self._srcDir = configs.getsrc()
        self._sftpHost = configs.gethost()
        self._sftpPort = configs.getport()
        self._sftpUsername = configs.getuser()
        self._sftpSecret = configs.getsecret()
        self._destDir = configs.getdest()

    def upload(self) -> list:
        """
        Connects to SFTP host and transfers files passed as an input

        Returns
        --------
        list
            a list of uploaded files

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
            _sftp.chdir(self._destDir)

            _start = current_time_in_millis()
            # audit_params(operation=Sc.OPERATION_UPLOAD,
            #              status=Sc.STATUS_PROCESSING,
            #              comments=Sc.MSG_FILES_UPLOADING)

            for file in self._files:
                _sftp.put(localpath=file,
                          callback=lambda transfered, size: audit_params(operation=Sc.OPERATION_UPLOAD,
                                                                         status=Sc.STATUS_COMPLETE,
                                                                         comments="{} {} ({})% ".format('<--<<', file, str("%.2f" % (100 * (int(transfered) / int(size)))))))

            # audit_params(operation=Sc.OPERATION_UPLOAD,
            #              status=Sc.STATUS_COMPLETE,
            #              comments=Sc.MSG_FILES_UPLOADED + time_taken(_start))
        finally:
            if _sftp is not None:
                _sftp.close()

        return self._files
