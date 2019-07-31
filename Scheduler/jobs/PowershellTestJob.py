from jobs.Job import Job


class PowershellTestJob(Job):

    def name(self) -> str:
        return 'PowershellTestJob-01'

    def goal(self):
        pass

