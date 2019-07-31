import requests
from requests import Response
from auditlogging.Trail import Trail
from utils.Utils import is_empty
from auditlogging.agents.AuditAgent import AuditAgent


class APIAuditAgent(AuditAgent):
    """
    Captures the audit trail using a REST endpoint URL (POST)
    Add this agent to Auditor in order to capture audit log to an endpoint.

    Note
    -----------
    1. If user wants to POST custom JSON request body then,
        pass a valid JSON string to constructor and call Auditor.audit_custom(your_custom_json)
    2. After each call to capture() or capture_custom() latest response is preserved
        until next endpoint request.
        To get the response, after each invocation please call endpoint_response() to get response

    """

    def __init__(self):
        self._url = 'http://localhost:3000/auditlogs/create'
        self._resp = None

    def change_endpoint(self, url: str):
        """
        Changes the default POST endpoint URL.
        Caller can specify any POST endpoint URL to create resource in
        database/storage.

        Parameters
        ----------
        url : str
              a new POST endpoint URL

        """
        if not is_empty(url):
            self._url = url

    def capture(self, trail: Trail):
        """
        Capture Trail to endpoint. Internally it transforms JSON
        object while calling POST endpoint

        Parameters
        ----------
        trail : Trail
                a trail object to be used for POST

        """
        self._call_endpoint(trail)

    def capture_custom(self, jsontrail: str):
        """
        Capture custom JSON trail to endpoint

        Parameters
        ----------
        jsontrail : str
                    custom JSON required for

        """
        self._mark_json_trail(jsontrail)

    def endpoint_response(self) -> Response:
        """
        access the response of the endpoint URL

        Returns
        --------
        Response
            Http response

        """
        return self._resp

    def _set_response(self, resp: Response):
        self._resp = resp

    def _call_endpoint(self, trail: Trail):

        _resp = requests.post(self._url, json=trail.build_trail())

        if _resp.status_code is not 200:
            print(_resp.json())

        self._set_response(resp=_resp)

    def _mark_json_trail(self, jsontrail: str):
        _resp = requests.post(self._url, data=jsontrail)

        self._set_response(resp=_resp)
