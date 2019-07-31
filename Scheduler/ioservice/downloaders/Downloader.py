from abc import ABCMeta, abstractmethod


class Downloader(metaclass=ABCMeta):
    """
    An abstract class provides a template for download activities.
    A subclass must provide implementation for download operation.

    Examples
    --------
    1. Files download from SFTP or remote location
    2. Files copy from one directory to another

    """

    @abstractmethod
    def download(self) -> list:
        """
        An abstract method for all download or copy operations

        Returns
        --------
        list
            a list for files downloaded

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
