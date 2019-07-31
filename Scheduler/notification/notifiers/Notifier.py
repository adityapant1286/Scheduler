from abc import ABCMeta, abstractmethod


class Notifier(metaclass=ABCMeta):
    """
    Provides a template to a subsclass to provide implementation for notification

    """

    @abstractmethod
    def notify(self):
        """
        A subclass must provide implementation to notification

        """
        raise NotImplementedError

