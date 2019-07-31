import configs.ConfigLoader as ConfigLoader
import utils.Constants as Sc
from scheduling.Scheduler import Scheduler
from scheduling.ScheduleConfig import ScheduleConfig
from jobs.TestJob import TestJob
# from jobs.LoadOrdersJob import LoadOrdersJob


# def _test_cases(_scheduler: Scheduler):
#     _job1 = TestJob(job_name='TestJob-1', text='Aditya')
#     sconfig = ScheduleConfig(every=1, time_unit=Sc.MINUTES)
#     _scheduler.schedule_job(job=_job1, schedule_config=sconfig, run_continuous=True)
#
#     _job2 = TestJob(job_name='TestJob-2', text='Adi')
#     _scheduler.schedule_job(job=_job2, schedule_config=sconfig, pulse_seconds=5, run_continuous=False)


# bootstrap sequence
# step 1 - prepare all audit agents

# step 2 - load configurations
# ConfigLoader.reload_config(which_env=Sc.ENV_DEV)
#
# if ConfigLoader.is_valid():
#     # step 3 - schedule jobs
#     scheduler = Scheduler()
#     _test_cases(scheduler)
#     # _job = LoadOrdersJob()
#     # scheduler.schedule_job(job=_job, pulse_seconds=30, run_continuous=True)
#     # step 4 - start scheduler
#     scheduler.start()
# else:
#     print(Sc.ERR_MSG_STARTUP)
#

# def _scheduler() -> Scheduler:
#     return scheduler
