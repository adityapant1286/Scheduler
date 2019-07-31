"""
This module provides various features for scheduling jobs.
Following are the features provided by this module.

* Scheduling a job - we could add multiple jobs for schedule. Can be run continuously
* Cancelling a job with the job identifier
* Retrieve the next schedule run time
* Start scheduler
* Shutdown scheduler - default safe-shutdown, user can *force* shutdown

Tip
---

+-------------+-------------------+-------------------+
|  Time unit  |     Every         |     At            |
+=============+===================+===================+
|  minute     |        -          |        -          |
+-------------+-------------------+-------------------+
|  hour       |        -          |        -          |
+-------------+-------------------+-------------------+
|  second     |        -          |        -          |
+-------------+-------------------+-------------------+
|  minutes    |     Numeric       |        -          |
+-------------+-------------------+-------------------+
|  hours      |     Numeric       |        -          |
+-------------+-------------------+-------------------+
|  seconds    |     Numeric       |        -          |
+-------------+-------------------+-------------------+
|  monday     |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  tuesday    |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  wednesday  |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  thursday   |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  friday     |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  saturday   |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+
|  sunday     |        -          |  00:00 - 23:59    |
+-------------+-------------------+-------------------+

Note
----
Since there is no synchronize mechanism between one or more scheduler instances,
running 2 instances for the same job has adverse effects. For an instance,
if the job is writing data into a database. Failure is bound to occur on the second
instance of the scheduler due to data redundancy error from database.
To resolve this issue, please modify configurations or a job for the second instance
and then run 2 instances.

Important
---------
Assuming a job is transferring files from one location to another.
Assuming the whole process takes 5 minutes in total. Scheduling the job every 2 minutes will
cause errors due to another same job is already running.
Therefore while scheduling a job, please analyse the maximum time required to complete a job.
Then set the maximum interval plus additional buffer time, to avoid race condition.
You could schedule a job to run once to understand the time required to finish the job.

Examples
--------
1. Schedule a job which runs every minute, in main thread.

    | ``EVERY = 1, TIME_UNIT = minutes``
    | ``sche = Scheduler()``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1, run_continuous=True)``
    | ``sche.start()``

2. Schedule a job which runs every hour, in separate thread.

    | ``EVERY = 1, TIME_UNIT = hours``
    | ``sche = Scheduler(separate_thread=True)``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1, run_continuous=True)``
    | ``sche.start()``

3. Schedule a job which runs once everyday, in main thread.
   The scheduler will make best efforts to run the job at 00:00 default time of the day.

    | ``TIME_UNIT = day``
    | ``sche = Scheduler()``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1, run_continuous=True)``
    | ``sche.start()``

4. Schedule a job which runs at 10:00 every Friday, in main thread.

    | ``AT = 10:00, TIME_UNIT = friday``
    | ``sche = Scheduler()``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1, run_continuous=True)``
    | ``sche.start()``

5. Schedule a job which run once only on Wednesday, in main thread.
   The scheduler will make best efforts to run the job at 00:00 default time of the day.

    **Note**
    You should have guessed, that the scheduler must be running in order
    to execute this job on Wednesday. If the job scheduled on Friday, then
    scheduler should keep running for 5 days to execute a job on Wednesday

    | ``TIME_UNIT = wednesday``
    | ``sche = Scheduler()``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1)``
    | ``sche.start()``

6. Schedule a job which run once only at 21:00 on Wednesday, in main thread.

    **Note**
    You should have guessed, that the scheduler must be running in order
    to execute this job on Wednesday as 21:00. If the job scheduled on Friday, then
    scheduler should keep running for 5 days to execute a job on Wednesday

    | ``AT = 21:00, TIME_UNIT = wednesday``
    | ``sche = Scheduler()``
    | ``job1 = TestJob()``
    | ``sche.schedule_job(job=job1)``
    | ``sche.start()``

"""

import configs.ConfigConstant as Cc
import utils.Constants as Sc
from scheduling.ScheduleConfig import ScheduleConfig
from utils.Utils import cfg, is_valid_implementation, isnone, is_empty
from jobs.Job import Job
from auditlogging.Auditor import audit_params
from utils.StringBuilder import StringBuilder

import schedule
import time
import threading
import inspect


class Scheduler:

    __counter = int(0)
    __instances = {}

    @staticmethod
    def all_instances() -> dict:
        """
        Get all instances of ``Scheduler`` created on this machine.
        ``Key=Scheduler-[counter], Value=[instance of Scheduler]``

        Returns
        -------
        dict
            a map of scheduler instances

        """
        return Scheduler.__instances

    @staticmethod
    def find_instance(instance_id: str = None):
        """
        This function returns a Scheduler instance mapped to an ``instance_id``.
        If ``instance_id`` is a number, it will add prefix *Scheduler-* before searching to collection.

        Examples
        --------
        | 1. ``inst = Scheduler.instance_by(instance_id='1')``
        | 2. ``inst = Scheduler.instance_by(instance_id='Scheduler-1')``

        Parameters
        ----------
        instance_id : str
                        a Scheduler instance id to be search for

        Returns
        -------
        Scheduler
                if present then instance of mapped Scheduler

        Raises
        ------
        ValueError
                if ``instance_id`` is None or Empty

        """
        if is_empty(instance_id):
            raise ValueError("instance_id must be provided and should not be empty")

        if Scheduler._is_number(instance_id):
            instance_id = str('Scheduler-' + instance_id)

        return Scheduler.all_instances().get(instance_id)

    def __init__(self, separate_thread: bool = False):
        """
        Initiates default properties for scheduler which a user can set dynamically by changing its behaviour.
        Scheduler interval and time unit retrieved from configurations.

        Parameters
        ----------
        separate_thread : bool
                          indicates whether to run scheduler jobs in a separate thread
                          or in the ``main`` thread. Default False = ``main`` thread.

        """
        self._every = cfg(Cc.EVERY)
        self._unit = cfg(Cc.TIME_UNIT)
        self._at_time = cfg(Cc.AT)
        self._next_run = None
        self._idle_seconds = None
        self._separate_thread = separate_thread
        self._stop_event = None
        self._run_continuous = False
        self._pulse = 0
        self._print_etr = True
        self._shutdown_requested = False
        self._started = False
        self.__wait = False
        __next_id = str(Scheduler.__counter + 1)
        self._instance_id = 'Scheduler-' + __next_id
        Scheduler.__instances[self._instance_id] = self

    def instance_id(self):
        """

        Returns
        -------
        str
            ``instance_id`` of current instance

        """
        return self._instance_id

    def schedule_job(self, job: Job, schedule_config: ScheduleConfig = None, run_continuous: bool = False,
                     execute_parallel: bool = False, pulse_seconds: int = Sc.DEFAULT_PULSE):
        """
        Schedules a job with ``name`` and user can specify whether the job should run once or should run continuously.

        Parameters
        ----------
        job : Job
              an instance of custom implementation of the ``Job`` module. Default ``None``
        schedule_config : ScheduleConfig
                        if user wants to change the ``every`` or ``at`` and ``time_unit`` before job schedule,
                        then user can create an instance on ScheduleConfig and specify new values
                        for schedule
        run_continuous : bool
                        if ``True`` the scheduler will continuously run jobs as per schedule,
                        run jobs once otherwise
        execute_parallel : bool
                            if ``True`` the job will be scheduled to execute parallel by spawning a thread,
                            sequential otherwise
        pulse_seconds : int
                       seconds to keep checking next schedule. Default 5 seconds.

                       Examples
                       --------
                        1. ``pulse_seconds=10`` will check next scheduler every 10 seconds
                        2. ``pulse_seconds=30`` will check next scheduler every 30 seconds

        """

        if not is_valid_implementation(job, Job):
            raise Exception(Sc.MSG_EX_ILLEGAL_JOB)

        if not isnone(schedule_config):
            self._override_schedule(schedule_config)

        self._run_continuous = run_continuous
        self._pulse = pulse_seconds

        audit_params(Sc.OPERATION_SCHEDULE, Sc.STATUS_SCHEDULING, 'Scheduling a job')

        if not isnone(self._every):
            evaluation_str = 'schedule.every(int(self._every)).' + self._unit
        else:
            evaluation_str = 'schedule.every().' + self._unit

        job_name = job.name()

        evaluation_str += self._at()
        if execute_parallel:
            evaluation_str += '.do(self._spawn_thread, job.goal).tag(job_name)'
        else:
            evaluation_str += '.do(job.goal).tag(job_name)'

        eval(evaluation_str)

        comments = StringBuilder(', ')
        comments.append('A job scheduled. Summary (Every=' + str(self._every)) \
            .append('TimeUnit=' + str(self._unit)) \
            .append('At=' + str(self._at_time)) \
            .append('SeparateThread=' + str(self._separate_thread)) \
            .append('RunningContinuously=' + str(self._run_continuous)) \
            .append('Pulse=' + str(self._pulse) + ')')

        audit_params(Sc.OPERATION_SCHEDULE, Sc.STATUS_SCHEDULED, comments.to_string())

        print(Sc.MSG_JOB_SCHEDULED)

    def _spawn_thread(self, goal):
        _job_thread = threading.Thread(target=goal)
        _job_thread.start()

    def _override_schedule(self, schedule_config: ScheduleConfig):
        """
        User must not provide values for both Every and At, this will result in ValueError.
        After validating it overides time unit, every or at

        Parameters
        ----------
        schedule_config : ScheduleConfig
                            a job specific schedule configurations. Every or At and/or Time Unit.

        Raises
        ------
        ValueError
            If values for every and at are provided (both), then this rejects scheduling the job

        """
        if not schedule_config.is_valid():
            raise ValueError(Sc.MSG_EX_INVALID_SCHEDULE_CONFIG)

        self._unit = schedule_config.time_unit()

        if not isnone(schedule_config.every()):
            self._every = schedule_config.every()

        elif not is_empty(schedule_config.at()):
            self._at_time = schedule_config.at()

    def cancel_job(self, job_name: str):
        """
        Cancels a job from scheduler. Calling this methods has no effect, if scheduler shutdown is requested
        before calling this method.

        Parameters
        ----------
        job_name : str
                   a job identifier set during a job schedule

        """
        if not isnone(job_name) and not self._shutdown_requested:
            schedule.clear(job_name)

    def what_is_next_run(self):
        """
        Retrieves next job run schedule

        Returns
        --------
        object
            next run schedule

        """
        return self._next_run

    def start(self, print_next_run=True):
        """
        Starts the scheduler as per the configurations and parameters. Calling this method more than once has
        no effect if ``shutdown`` requested or already started.
        If ``separate_thread`` is true, then scheduler will run in separate thread, ``main`` thread otherwise.
        If ``run_continuous`` is true, then job will be run continuously, once otherwise

        Parameters
        ----------
        print_next_run : bool
                         if ``True`` it will keep printing next rnu schedule at every ``pulse_seconds``.
                         Default every 5 seconds

        """
        if self._shutdown_requested or self._started:
            return

        print('Starting scheduler > ')

        self._print_etr = print_next_run

        audit_params(Sc.OPERATION_START_JOBS, Sc.STATUS_STARTING, 'Starting scheduled jobs')

        if self._separate_thread:
            self._stop_event = self._schedule_in_separate_thread()
        else:
            self._schedule_in_main_thread()

    def shutdown(self, force: bool = False):
        """
        Shuts down the scheduler. When requested, calling cancel any job has no effect.

        Parameters
        ----------
        force : bool
                if ``True`` it will not wait until the jobs complete, otherwise will wait until
                all jobs complete and then safely shutdown

        """

        if inspect.stack()[1].function != '_shut_it_down':
            return

        print(Sc.MSG_SHUTTING_DOWN_SCHEDULER)
        audit_params(Sc.OPERATION_SHUTDOWN, Sc.STATUS_STARTING, Sc.MSG_SHUTTING_DOWN_SCHEDULER + ' Force=' + str(force))

        if self._run_continuous:
            self.__wait = True
            self._shutdown_requested = True
            if self._separate_thread:
                self._stop_event.set()
            else:
                self._run_continuous = False

            if not force:
                self._wait_until_safely_shutdown()
        schedule.clear()

        audit_params(Sc.OPERATION_SHUTDOWN, Sc.STATUS_COMPLETE, Sc.MSG_SCHEDULER_SHUTDOWN_COMPLETE)

        print(Sc.MSG_SCHEDULER_SHUTDOWN_COMPLETE)

    def _wait_until_safely_shutdown(self):
        """
        If not force shutdown, then this method will ensure all jobs will complete before shutdown safely.

        """
        audit_params(Sc.OPERATION_SHUTDOWN, Sc.STATUS_WAITING, Sc.MSG_WAIT_UNTIL_SAFE_SHUTDOWN)
        while self.__wait:
            print("Please wait...")
            time.sleep(2)

    def _schedule_in_main_thread(self):
        """
        Run scheduler in the main thread.
        If ``run_continuous`` is true then it will continuously run the jobs on schedule.
        Otherwise run all jobs at once.

        """

        if self._run_continuous:
            audit_params(Sc.OPERATION_START_JOBS, Sc.STATUS_STARTED, Sc.MSG_JOB_STARTED.format(str(self._print_etr)))
            self._started = True
            while True:
                try:
                    if not self._run_continuous:
                        print(Sc.MSG_SHUTDOWN_SCHEDULER_RUNNING_ALL)
                        schedule.run_all()
                        self.__wait = False
                        self._shutdown_requested = False
                        self._started = False
                        break

                    self._next_run = schedule.next_run()
                    self._idle_seconds = schedule.idle_seconds()
                    self._log_etr()

                    schedule.run_pending()

                    time.sleep(self._pulse)
                except KeyboardInterrupt:
                    audit_params(operation=Sc.OPERATION_SHUTDOWN,
                                 status=Sc.STATUS_INTERRUPTED,
                                 comments=Sc.MSG_SCHEDULER_INTERRUPTED)
                    schedule.run_all()
                    self.__wait = False
                    self._shutdown_requested = False
                    self._started = False
                    break
        else:
            audit_params(Sc.OPERATION_START_JOBS, Sc.STATUS_STARTED, Sc.MSG_JOB_STARTED.format(str(self._print_etr)))
            schedule.run_all()
            # time.sleep(self._pulse)

    def _schedule_in_separate_thread(self) -> threading.Event:
        """
        Run scheduler in a separate thread written in inner class.
        If ``run_continuous`` is true then it will continuously run the jobs on schedule.
        Otherwise run all jobs at once.

        Parameters
        ----------
        threading.Event
                        A threading event which will later use to safely shutdown scheduler

        """
        stop_continuous_run = threading.Event()

        class SeparateThread(threading.Thread):
            @classmethod
            def run(cls):
                if self._run_continuous:
                    audit_params(Sc.OPERATION_START_JOBS, Sc.STATUS_STARTED,
                                 Sc.MSG_JOB_STARTED.format(str(self._print_etr)))
                    self._started = True
                    while True:
                        try:
                            if stop_continuous_run.is_set():
                                print(Sc.MSG_SHUTDOWN_SCHEDULER_RUNNING_ALL)
                                schedule.run_all()
                                self.__wait = False
                                self._shutdown_requested = False
                                self._started = False
                                break

                            self._next_run = schedule.next_run()
                            self._idle_seconds = schedule.idle_seconds()
                            self._log_etr()

                            schedule.run_pending()

                            time.sleep(self._pulse)
                        except KeyboardInterrupt:
                            audit_params(operation=Sc.OPERATION_SHUTDOWN,
                                         status=Sc.STATUS_INTERRUPTED,
                                         comments=Sc.MSG_SCHEDULER_INTERRUPTED)
                            self._stop_event.set()
                            schedule.run_all()
                            self.__wait = False
                            self._shutdown_requested = False
                            self._started = False
                            break
                else:
                    audit_params(Sc.OPERATION_START_JOBS, Sc.STATUS_STARTED,
                                 Sc.MSG_JOB_STARTED.format(str(self._print_etr)))
                    schedule.run_all()
                    # time.sleep(self._pulse)

        continuous_thread = SeparateThread()
        continuous_thread.start()

        return stop_continuous_run

    def _at(self):
        """
        If at is provided then this method will set the clock time on schedule.

        Returns
        --------
        str
            a schedule having clock time set, blank if every is provided

        """
        if not is_empty(self._at_time) \
                and not Scheduler._is_number(self._at_time) \
                and ":" in self._at_time:
            print('time clock')
            return '.at(self._at_time)'
        return ''

    def _log_etr(self):
        """
        Prints Estimated Time to Next Run and remaining time (in seconds) on console

        """
        if self._print_etr:
            # __nextrun = self._next_run
            # remaining_time = self._next_run - datetime.datetime.now()
            print(Sc.MSG_NEXT_RUN_SCHEDULE.format(str(self._next_run), str(self._idle_seconds)))

    @staticmethod
    def _is_number(x):
        try:
            int(x)
            return True
        except ValueError:
            return False
