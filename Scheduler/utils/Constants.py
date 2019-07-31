"""
All module related constants definitions in one place. It allows to modify values without changing the underlying code.
Having them at one place makes easier to manage. Also prevents redundant strings or numeric values.

1. CONFIG_FILE = Scheduler configuration file path. This allows to place the configurations to different directory.
2. The environment key should be used to acquire related configurations. Valid values [ENV_DEV, ENV_TEST, ENV_PROD]
3. Information messages key should start from MSG
4. Exception messages key should start from MSG_EX
5. Error messages key should start from ERR_MSG
6. All operations performed by scheduler, the key should start from OPERATION
7. All statuses assigned by scheduler, the key should start from STATUS
8. All default values used for scheduler operations, the key should start from DEFAULT

"""

# configs
CONFIG_FILE = "/config.yaml"
ENV_DEV = "DEV"
ENV_TEST = "TEST"
ENV_PROD = "PROD"

# messages
# messages > Info
MSG_CONFIG_LOADING = "\n(i) Loading scheduler configurations..."
MSG_CONFIG_LOADED = "(i) Scheduler configurations loaded!\n"
MSG_FILES_DOWNLOADED = "(i) Files downloaded"
MSG_FILES_DOWNLOADING = "\n(i) Files downloading. Please wait..."
MSG_FILES_TRANSFERRING = "\n(i) Transferring files, please wait..."
MSG_FILES_TRANSFERRED = "(i) Files transfer complete "
MSG_FILES_UPLOADED = "(i) Files uploaded"
MSG_FILES_UPLOADING = "\n(i) Files uploading. Please wait..."
MSG_JOB_SCHEDULED = "(i) Job has been scheduled and ready to start."
MSG_NEXT_RUN_SCHEDULE = "(i) Next job to run at {}, which is {} seconds from now"
MSG_JOB_STARTED = "Scheduled jobs started and will run on schedule. (Print Estimated Time to Run (ETR)= {})"
MSG_SHUTTING_DOWN_SCHEDULER = "(i) Shutting down scheduler..."
MSG_WAIT_UNTIL_SAFE_SHUTDOWN = "(i) Waiting until safely shutdown. " \
                               "NOTE: This operation will complete all pending jobs and then shutdown."
MSG_SHUTDOWN_SCHEDULER_RUNNING_ALL = "(i) Running all pending jobs before shutting down scheduler..."
MSG_SCHEDULER_SHUTDOWN_COMPLETE = "(i) Scheduler shutdown complete."
MSG_FORCE_STOP = "(i) Force stopping scheduler..."
MSG_SCHEDULER_INTERRUPTED = "*** (><) Scheduler interrupted, trying to safely shutdown. " \
                            "All pending jobs will be executed immediately."
# messages > exception
MSG_EX_ILLEGAL_DOWNLOADER = "(EX) Illegal downloader argument"
MSG_EX_ILLEGAL_UPLOADER = "(EX) Illegal uploader argument"
MSG_EX_ILLEGAL_NOTIFIER = "(EX) Illegal notifier argument"
MSG_EX_ILLEGAL_JOB = "(EX) Illegal job argument"
MSG_EX_INVALID_SCHEDULE_CONFIG = "(EX) Either 'every' or 'at' should be provided, " \
                                 "not both. Job rejected due to invalid schedule configurations."
# messages > Error
ERR_MSG_INVALID_CONFIGS = "(X) *** Invalid configurations present, " \
                          "please resolve errors to be able to start scheduler ***"
ERR_MSG_STARTUP = "(X) *** Please fix configurations to initiate scheduler startup."
ERR_MSG_DIR_EMPTY = "(X) Source and target directories are mandatory"
ERR_MSG_ERR_DIR_EMPTY = "(X) Error and output directories are mandatory"
ERR_MSG_REMOTE_CFG_EMPTY = "(X) Source host, username, secret are mandatory for remote"
ERR_MSG_SCHEDULE_ACTION_EMPTY = "(X) Schedule and action are mandatory"
ERR_MSG_SMTP_INVALID = "(X) Invalid SMTP or Email configurations"
ERR_MSG_SCHEDULE_INVALID = "(X) Invalid schedule configurations. Value for both EVERY and AT are not allowed," \
                           " it should be either one."
ERR_MSG_TIME_UNIT_EMPTY = "(X) At least one Time Unit should be present."
# messages > Audit
# messages > Audit > operation
OPERATION_CONFIGURATION = "Configuration"
OPERATION_CREATE = "Create"
OPERATION_UPDATE = "Update"
OPERATION_DOWNLOAD = "Download"
OPERATION_UPLOAD = "Upload"
OPERATION_FILE_DELETE = "File-Delete"
OPERATION_FILE_TRANSFER = "File-Transfer"
OPERATION_NOTIFICATION = "Notification"
OPERATION_SCHEDULE = "Scheduler"
OPERATION_START_JOBS = "Start-Jobs"
OPERATION_SHUTDOWN = "Shutdown"

# messages > Audit > status
STATUS_LOADED = "Loaded"
STATUS_LOADING = "Loading"
STATUS_INVALID = "Invalid"
STATUS_PROCESSING = "Processing"
STATUS_COMPLETE = "Complete"
STATUS_SCHEDULING = "Scheduling"
STATUS_SCHEDULED = "Scheduled"
STATUS_STARTING = "Starting"
STATUS_STARTED = "Started"
STATUS_WAITING = "Waiting"
STATUS_INTERRUPTED = "Interrupted"

# default configs
DEFAULT_SCHEDULER_ACTION = "create"
DEFAULT_PULSE = 5
DEFAULT_SFTP_PORT = 22

# constants
C_TIME_PARTS = {"hour", "minute", "second"}
CREATE = 'CREATE'
UPDATE = 'UPDATE'

# email notifier
SUBJECT = "Subject"
FROM = "From"
TO = "To"
DATE = "Date"
CONTENT_DISPOSITION_K = "Content-Disposition"
CONTENT_DISPOSITION_V = 'attachment; filename="%s"'

SECOND = 'second'
SECONDS = 'seconds'
MINUTE = 'minute'
MINUTES = 'minutes'
HOUR = 'hour'
HOURS = 'hours'

DAY = 'day'

MONDAY = 'monday'
TUESDAY = 'tuesday'
WEDNESDAY = 'wednesday'
THURSDAY = 'thursday'
FRIDAY = 'friday'
SATURDAY = 'saturday'
SUNDAY = 'sunday'
