from jobs.Job import Job


class TestJob(Job):

    def __init__(self, job_name: str, text: str):
        self._text = text
        self._job_name = job_name

    def goal(self):
        print("Hello from test job " + str(self._text))

    def name(self) -> str:
        return self._job_name
