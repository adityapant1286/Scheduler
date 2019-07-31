import getpass


class HostConfig:
    """
    A data model class which holds custom configurations for different IO services.
    A subclass of either Cleaner or Downloader tor Uploader can use this class to hold connectivity
    details or additional file parameters.
    This class implements a builder pattern where a developer can set required values to an object.

    """

    def __init__(self):
        self._config = {}

    def append(self, k, v):
        """
        Optionally a developer can use this method to append as many as
        custom config which can be retrieved using key.
        Please use get(k) method to retrieve a custom value of a key.

        Parameters
        ----------
        k : str
            a key to be used to identify its value
        v : object
            a value associated to key

        Returns
        --------
        HostConfig
            instance of this object

        """
        self._config[str(k)] = v
        return self

    def src(self, v):
        """
        Sets source directory or file depending on implementation of a subclass

        Parameters
        ----------
        v : object
            an associated source directory or file

        Returns
        ----------
        HostConfig
            instance of this object

        """
        return self.append('src', v)

    def host(self, v):
        """
        Sets host name or IP address

        Parameters
        ----------
        v : object
            an associated host name or IP address

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('host', v)

    def port(self, v):
        """
        Sets port number of a host

        Parameters
        ----------
        v : object
            an associated host port number

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('port', v)

    def user(self, v):
        """
        Sets username which will be used to connect to a host

        Parameters
        ----------
        v : object
            an associated username of a host

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('user', v)

    def secret(self, v):
        """
        Sets either password string or SSH private key location path or an OAUTH token, which will be
        used to connect to a host along with username

        Parameters
        ----------
        v : object
            an associated password string or SSH private key location path or OAUTH token

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('secret', v)

    def dest(self, v):
        """
        Sets destination directory or file depending on implementation of a subclass

        Parameters
        ----------
        v : object
            an associate destination directory or file

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('dest', v)

    def fileext(self, v: list):
        """
        Sets a list of file extensions which could be used to filter files

        Parameters
        ----------
        v : object
            an associated list of file extensions

        Returns
        --------
        HostConfig
            instance of this object

        """
        return self.append('extn', v)

    def build(self):
        """
        Optional: constructs and returns final HostConfig object having
                key=values set before calling this method

        Returns
        --------
        HostConfig
            a constructed HostConfig object

        """
        return self._config

    def get(self, k: str, _default=None):
        """
        Developer should use this method if any custom configurations are appended to this HostConfig.
        For all predefined configurations a developer should call corresponding method
        to avoid exception due to invalid key.

        Parameters
        ----------
        k : str
            a key to be searched in configuration
        _default : object
                    a default value should be returned if specified key not found.
                    If not provided then default None

        Returns
        --------
        object
            a value associate to key if present, default otherwise

        """
        return self._config.get(k, _default)

    def getsrc(self) -> str:
        """
        Retrieves source directory or file path

        Returns
        --------
        str
            if set then returns source directory or file path,
            current directory '.' path otherwise

        """
        return str(self.get('src', '.'))

    def getdest(self) -> str:
        """
        Retrieves destination directory or file path

        Returns
        --------
        str
            if set then returns destination directory or file path,
            current directory '.' path otherwise

        """
        return str(self.get('dest', '.'))

    def gethost(self) -> str:
        """
        Retrieves host name or IP address

        Returns
        --------
        str
            if set then returns host name or host IP address, '127.0.0.1' otherwise

        """
        return str(self.get('host', '127.0.0.1'))

    def getport(self) -> int:
        """
        Retrieves host port number

        Returns
        --------
        int
            if set then returns host port number, 22 otherwise

        """
        return int(str(self.get('port', 22)))

    def getuser(self) -> str:
        """
        Retrieves host username

        Returns
        --------
        str
            if set then returns host username, current username otherwise

        """
        return str(self.get('user', getpass.getuser()))

    def getsecret(self) -> str:
        """
        Retrieves password or SSH private key location path or OAUTH token of the host username

        Returns
        --------
        object
            if set then returns host password or SSH private key location path or OAUTH token,
            None otherwise

        """
        return str(self.get('secret', ''))

    def getfile_ext(self) -> object:
        """
        Retrieves a list of file extensions to be used for filter

        Returns
        --------
        object
            if set then returns a list of file extensions, blank string otherwise

        """
        return self.get('extn', [])

