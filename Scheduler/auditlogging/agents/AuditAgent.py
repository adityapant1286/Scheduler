from abc import ABCMeta, abstractmethod
from auditlogging.Trail import Trail


class AuditAgent(metaclass=ABCMeta):
    """
    This class will be used to create a custom audit capture agent.
    A DefaultAgent class has been created for a reference, which will be used for default behaviour along with
    other custom AuditAgents

    """

    @abstractmethod
    def capture(self, trail: Trail):
        """
        Subclass must implement this method to customize Audit capture.

        Parameters
        ----------
        trail : Trail
                Contains fields to be capture for audit

        """
        raise NotImplementedError

    @abstractmethod
    def capture_custom(self, jsontrail: str):
        """
        Subclass must implement this method to customize Audit capture.

        Parameters
        ----------
        jsontrail : str
                    contains fields to be capture for audit

        """
        raise NotImplementedError

