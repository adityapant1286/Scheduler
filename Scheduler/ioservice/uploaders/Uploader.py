from abc import ABCMeta, abstractmethod


class Uploader(metaclass=ABCMeta):
    """
    An abstract class provides a method to write a custom implementation
    for upload operation, either from localhost to remote SFTP or transfer file from one directory to archive.

    """

    @abstractmethod
    def upload(self) -> list:
        """
        A subclass must provide upload implementation as per the requirements

        Returns
        --------
        list
            a list of files uploaded

        """
        raise NotImplementedError

    @abstractmethod
    def change_dir(self, src: str, dest: str):
        """
        Overrides the source and/or destination directory

        Parameters
        ----------
        src : str
                source directory path
        dest : str
                destination directory path

        """
        raise NotImplementedError

    @abstractmethod
    def change_files(self, files: list):
        """
        Overrides a list of files to be used to perform IO operations.
        It is usefull when user just wants to pass a new list of files.

        Parameters
        ----------
        files
            a new list of files

        """
        raise NotImplementedError
