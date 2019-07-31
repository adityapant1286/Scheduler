

class ScheduleConfig:

    def __init__(self, every: int = None, time_unit: str = 'hour', at: str = None):
        """
        Creates an immutable instance of schedule configurations which will be used to change scheduler behaviour
        at runtime by modifying ``every`` or ``at`` and ``time_unit``.

        Danger
        ------
        Providing `every` and `at` both the value will prevent scheduling a job due to conflicts with time units.
        User can also schedule a job by only providing the time unit. By default a job will execute once per time unit.

        Parameters
        ----------
        every : int
                This numeric value represents number of times a job will execute per time unit.
                Time unit are conditionally valid depending on this value.

        time_unit : str
                    This value indicates whether a job should run number of times per unit or at per unit.

                    Tip
                    ---
                    * in case the value for every is provided then, - seconds, minutes, hours, day (plurals)
                    * in case only time unit provided then, - second, minute, hour, day (singular)
                    * in case the time string for at is provided then, day, monday, tuesday, wednesday,
                        thursday, friday, saturday, sunday

        at : str
            a string represents at specified time a job will execute on
            per time unit. If a value provided for `every` then avoid providing a value for this field.

        """
        self._every = every
        self._time_unit = time_unit
        self._at = at

    def every(self) -> int:
        """
        Retrieves occurrence part from current instance

        Returns
        --------
        int
            number of times a job will execute per time unit

        """
        return self._every

    def time_unit(self) -> str:
        """
        Retrieves time unit string from current instance

        Returns
        --------
        str
            time unit string value

        """
        return self._time_unit

    def at(self) -> str:
        """
        Retrieves the clock time string from current instance

        Returns
        -------
        str
            clock time string from 00:00 to 23:59

        """
        return self._at

    def is_valid(self):
        """
        Validates value provided only for either `every` or `at` and not to both

        Returns
        -------
        bool
            True if either value provided. False otherwise

        """
        if not ScheduleConfig._isnone(self.every()) and not ScheduleConfig._is_empty(self.at()):
            return False
        else:
            return True

    @staticmethod
    def _isnone(o: object):
        return o is None

    @staticmethod
    def _is_empty(str1: str) -> bool:
        return ScheduleConfig._isnone(str1) or len(str1.strip()) == 0
