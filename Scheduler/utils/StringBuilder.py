

class StringBuilder:
    """
    This class implements a builder pattern which builds a string.

    Example
    --------
    1.  instance = StringBuilder()
        instance.append('Abc').append('def').append('xyz');
        print(instance.to_string())

        > Abcdefxyz
    2.  instance = StringBuilder('-')
        instance.append('Abc').append('def').append('xyz');
        print(instance.to_string())

        > Abc-def-xyz

    """

    def __init__(self, separator=''):
        """
        Create an instance with specified separator. Default empty string.

        Parameters
        ----------
        separator : str
                    a separator will be appended along with string

        """
        self._str = []
        self._separator = separator

    def append(self, s):
        """
        Appends a string to existing string
        
        Parameters
        ----------
        s : str
            a new string to append

        Returns
        --------
        StringBuilder
                    this string builder instance

        """
        self._str.append(str(s) + self._separator)
        return self

    def to_string(self) -> str:
        """
        Joins all strings together and returns as a single string

        Returns
        --------
        str
            joined string

        """
        joined = ''.join(self._str)
        return joined[:joined.rfind(self._separator)]

    def clear(self):
        """
        Clears all contents of string

        Returns
        -------
        StringBuilder
                current instance of StringBuilder

        """
        self._str.clear()
        return self

