import json as _complexjson


class Trail(object):
    """
    Trail model consists fields which will be store data.
    This class implements a builder pattern where a caller can build an object of this class.

    """

    def __init__(self):
        self._operation = None
        self._status = None
        self._comments = None

    def operation(self, operation: str):
        """
        Sets the operation to the trail instance

        Parameters
        ----------
        operation: str
                   An operation being performed or executed at the moment

        Returns
        --------
        Trail
            current instance of trail

        """
        self._operation = operation
        return self

    def status(self, status: str):
        """
        Sets the status to the trail instance

        Parameters
        ----------
        status : str
                 Current status of the operation being performed or executed at the moment

        Returns
        --------
        Trail
            current instance of trail

        """
        self._status = status
        return self

    def comments(self, comments: str = None):
        """
        Sets the comments to the trail instance. Default None.

        Parameters
        ----------
        comments : str
                   Additional comments relating to the operation

        Returns
        --------
        Trail
            current instance of trail

        """
        self._comments = comments
        return self

    def build_trail(self, formatted_json: bool = False):
        """
        This method should be invoke at the end when a constructed Trail object require

        Parameters
        ----------
        formatted_json : bool
                        if True then an object will be formatted using utility as JSON,
                        otherwise a string representation of Trail object in JSON format

        Returns
        --------
        str
            constructed Trail object in JSON format

        """
        payload = {'operation': self._operation, 'status': self._status, 'comments': self._comments}
        if formatted_json:
            return _complexjson.dumps(payload)
        else:
            return payload

