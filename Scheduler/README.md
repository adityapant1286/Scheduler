# Scheduler

### Summary

This module provides various features for scheduling jobs.
Following are the features provided by this module.

* Scheduling a job - we could add multiple jobs for schedule.
* One schedule all jobs or different schedule for different jobs.
* `Scheduler` can be run in a different isolated thread or in a main thread. 
* Jobs can be run continuously or once.
* Jobs can be scheduled to run parallel (different threads) or sequential per schedule.
* Cancelling a job with the job identifier.
* Retrieve the next schedule run time **Pre-requisite:** `Scheduler` should be set to run continuous.
* Start `Scheduler`.
* Shutdown `Scheduler` - default _safe-shutdown_, user can _force_ shutdown. By default Scheduler will complete all pending jobs, before finally shutdown.

### Configurations
As per requirements user can create multiple configuration sections in `config.yaml` file. _Example:_ _DEV_ (Development).
A user can create another section with the name as  _TEST_ for test environment configurations. 

NOTE: These configurations are one per instance of a `Scheduler` therefore any changes in this configurations requires a restart to apply changes.

Please see API documentation for more details.

### Prepare Scheduler
1. Clone repository on a machine.
2. Edit configurations in `Scheduler/configs/config.yaml` file based on the environment.

At this point the Scheduler is ready to accept scheduling any job.

### Creating a Job
1. Create a new python class and extend with `Scheduler/jobs/Job`. 
    This super class Job has two functions which a developer must override with implementation.
    Every job has a `name()` and `goal()` to be executed on each execution on schedule.
2. Override `name()` to provide a unique name for your job.
3. Override `goal()` to provide implementation of your use case to be performed by this job.
    You are free to create any private or protected functions and call inside the `goal()` function.
    Scheduler only invokes `goal()` function to perform the job operation.

### Scheduler Startup
1. Navigate to `Scheduler/startup.py` and open script
2. Load configurations by calling `ConfigLoader.reload_config(which_env=Sc.ENV_DEV)`. 
_Note:_ Please mention your environment to read specific configurations.
3. Create an instance of Scheduler. _Example:_ `sc = Scheduler(separate_thread)`. By default Scheduler runs in a main thread, setting `separate_thread=True` will run the Scheduler instance in a separate thread.
4. Create an instance of your job. _Example:_ `_job = TestJob()
_another = AnotherJob()`
5. Assign this job to scheduler. 
    - _Example:_ 
        1. One schedule for all jobs - 
            `sc.schedule_job(job=_job, run_continuous=True)` and `sc.schedule_job(job=_another)` 
            _Note:_ Observe that scheduling another job does not require to set `run_continuous=True` it has been derived from earlier job. 
            Setting it to False will override previous value and all jobs will run once only. You can create 2 instances of scheduler, one for running jobs continuous and another for running jobs once.
        2. Different schedule for different jobs - to override configuration schedule we need to create a `ScheduleConfig` object with necessary details then, pass on to _schedule_job()_. 
            i)  `sconfig = ScheduleConfig(every=10, time_unit=Sc.MINUTES)` `sc.schedule_job(job=_job, schedule_config=sconfig, run_continuous=True)` This will run on every 10 minutes.
           ii)  `sconfig = ScheduleConfig(every='14:00', time_unit=Sc.FRIDAY)` `sc.schedule_job(job=_job, schedule_config=sconfig, run_continuous=True)` This will run on every Friday at 14:00 (i.e. 2:00 pm).
6. Start the scheduler by calling _start()_. `sc.start()`

### Schedule Configurations

1. `EVERY` - a non zero numeric value which indicates number of times a job will run per time unit
2. `TIME_UNIT` - unit of time on which the _Scheduler_ will run a job.
    - Valid Values
        - second - value for EVERY and AT must be blank
        - seconds - value for AT must be blank
        - minute - value for EVERY and AT must be blank
        - minutes - value for AT must be blank
        - hour - value for EVERY and AT must be blank
        - hours - value for AT must be blank
        - day - value for either EVERY or AT or none
        - monday - value for either EVERY or AT or none
        - tuesday - value for either EVERY or AT or none
        - wednesday - value for either EVERY or AT or none
        - thursday - value for either EVERY or AT or none
        - friday - value for either EVERY or AT or none
        - saturday - value for either EVERY or AT or none
        - sunday - value for either EVERY or AT or none
3. `AT` - a clock time string at which a job should run per time unit. _Example:_ 14:00 

### Audit logging

Capturing audit log is vital for any business use case. 
This module provides a robust framework to capture audit log to different mediums or your custom medium.

There are following three APIs can be used as per requirements.
1. `Auditor.audit_params` - allows to capture standard fields for audit log. This function takes three mandatory parameters namely; operation, status and comments in string format.
2. `Auditor.audit_trail` - allows to capture a Trail object. This is overloaded API for the `audit_params`.
3. `Auditor.audit_custom` - allows to capture any JSON format object as a parameter for your custom POST API.

By default Auditor will capture audit logs on console, where a developer can 
