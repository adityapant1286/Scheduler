from auditlogging.agents.AuditAgent import AuditAgent
from auditlogging.Trail import Trail


class DefaultAgent(AuditAgent):
    """
    Custom implements of AuditAgent which prints the trail on console

    """

    def capture_custom(self, jsontrail: str):
        """
        Default agent only prints the output on the console

        Parameters
        ----------
        jsontrail : str
                    custom JSON object

        """
        print(jsontrail)

    def capture(self, trail: Trail):
        """
        Default functionality is to print the trail on console

        Parameters
        ----------
        trail : Trail
                a trail of information which will be printed on console

        """
        print(trail.build_trail())
