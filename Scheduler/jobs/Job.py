from abc import abstractmethod, ABCMeta


class Job(metaclass=ABCMeta):
    """
    An abstract class provides a method to specify a goal for a job which will be assigned to a scheduler.
    Developers are free to create any custom job which overrides ``goal`` method and assign to scheduler.
    This behaviour allows to plug in and out a job to and from scheduler.
    Please see ``Scheduler`` for more details.

    """

    @abstractmethod
    def goal(self):
        """
        A subclass must provide implementation for this methods

        """
        raise NotImplementedError

    @abstractmethod
    def name(self) -> str:
        """
        Subclass should provide implementation for this function

        Returns
        -------
        str
            Job name

        """
        raise NotImplementedError


