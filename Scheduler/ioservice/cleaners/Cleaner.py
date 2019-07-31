from abc import ABCMeta, abstractmethod


class Cleaner(metaclass=ABCMeta):
    """
    An abstract class which provides a template for cleanup
    activities.

    Example
    --------
    1. Directory cleanup when no longer needed
    2. Databased rows cleanup

    """

    @abstractmethod
    def clean(self):
        """
        A subclass must provide implementation for this method to perform any
        cleanup activities.

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
