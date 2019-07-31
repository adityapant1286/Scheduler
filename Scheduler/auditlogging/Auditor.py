from auditlogging.agents.AuditAgent import AuditAgent
from auditlogging.agents.DefaultAgent import DefaultAgent
from auditlogging.Trail import Trail


__agents = {}
_default_agent = DefaultAgent()


def add_agent(namekey: str, agent: AuditAgent):
    """
    Adds an AuditAgent to this Auditor

    Parameters
    ----------
    namekey : str
              AuditAgent identifier which will be used to remove
    agent : AuditAgent
            custom built AuditAgent

    """
    __agents[namekey] = agent


def remove_agent(namekey: str):
    """
    If present then, it removes AuditAgent from Auditor's agent collection.

    Parameters
    ----------
    namekey : str
              An AuditAgent to be removed

    """
    try:
        __agents.pop(namekey, None)
    except KeyError:
        print('{} not found'.format(namekey))


def audit_params(operation: str, status: str, comments: str):
    """
    Parameterised audit trail capture method. Internally Auditor will create a Trail object
    and assign to all AuditAgent

    Parameters
    ----------
    operation : str
                An operation being performed or executed at the moment
    status : str
             Current status of the operation being performed or executed at the moment
    comments : str
               Additional comments relating to the operation

    """
    trail = Trail()
    trail.operation(operation).status(status).comments(comments)
    _report_to_agents(trail)


def audit_trail(trail: Trail):
    """
    Pass on the trail to Audit agents

    Parameters
    ----------
    trail : Trail
            a trail instance

    """
    _report_to_agents(trail)


def audit_custom(jsontrail: str):
    """
    If you choosed to have your custom endpoint URL to capture
    Audit trail which has different JSON request body then,
    call this function

    Parameters
    ----------
    jsontrail : str
                a custom JSON string to be used as a request body for a POST endpoint

    """
    for agent in __agents.values():
        agent.capture_custom(jsontrail)


def _prepare_audit_agents():
    add_agent('Default-Agent', _default_agent)


def _report_to_agents(trail: Trail):
    for agent in __agents.values():
        agent.capture(trail)


_prepare_audit_agents()


