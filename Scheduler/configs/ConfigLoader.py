import yaml
import os
import configs.ConfigConstant as Cc
import utils.Constants as Sc
from auditlogging.Auditor import audit_params


class Box:
    pass


__box = Box()

__box.all_configs = None
__box.env = None
__box.valid = False


def reload_config(which_env=Sc.ENV_DEV):
    __box.env = which_env
    if __box.all_configs is None:
        _init()


def _init():
    """
    Initialise and load all configurations from file. This method also validates configurations for errors.

    """
    print(Sc.MSG_CONFIG_LOADING)

    audit_params(Sc.OPERATION_CONFIGURATION, Sc.STATUS_LOADING, 'Loading configurations from file')

    _working_dir = os.path.dirname(__file__)
    _scheduler_config_file = _working_dir + Sc.CONFIG_FILE

    # config_file_path = scheduler_config_file

    with open(_scheduler_config_file) as jf:
        __box.all_configs = yaml.load(jf)

    audit_params(Sc.OPERATION_CONFIGURATION, Sc.STATUS_LOADED, 'Loaded configurations from file')

    errors = _validate()
    __box.valid = _empty_arr(errors)

    if not __box.valid:
        audit_params(Sc.OPERATION_CONFIGURATION, Sc.STATUS_INVALID, 'Invalid configurations found')

    print(Sc.MSG_CONFIG_LOADED)


def env():
    """
    Retrieve current environment

    Returns
    --------
    str
        Current scheduler environment (DEV/TEST/PROD)

    """
    return __box.env


def all_configs():
    """
    Returns all loaded configurations including multiple environments, if any

    Returns
    ----------
    dictionary
            all configurations

    """
    return __box.all_configs


def all_by_environment():
    """
    Returns all configurations of the default environment

    Returns
    --------
    dictionary
            all configurations of default environment

    """
    return __box.all_configs.get(env())


def get_by_env(k: str, envp: str):
    """
    Searches the key inside the environment configurations and
    returns value if present

    Parameters
    ----------
    k : str
        a key to be search in configurations
    envp : str
            the key will be searched only in this environment

    Returns
    -------
    Object
        value of corresponding key, INVALID otherwise

    """
    return all_configs().get(envp).get(k, "INVALID")


def get(k: str):
    """
    Retrieves value of a key of the default environment

    Parameters
    ----------
    k : str
        a key to be search in configurations

    Returns
    --------
    object
        value of corresponding key if present, INVALID otherwise

    """
    if __box.all_configs is None or not __box.valid:
        reload_config()

    return all_by_environment().get(k, "INVALID")


def is_valid():
    """
    Returns whether configurations are valid which had checked during loading.

    Returns
    --------
    bool
        true if configurations are valid, false otherwise

    """
    return __box.valid


def _validate():
    """
    Validates configurations

    """
    errors = []

    if _empty(Cc.SOURCE_DIRECTORY) or _empty(Cc.TARGET_DIRECTORY):
        errors.append(Sc.ERR_MSG_DIR_EMPTY)

    if _empty(Cc.ERROR_DIRECTORY) or _empty(Cc.OUTPUT_DIRECTORY):
        errors.append(Sc.ERR_MSG_ERR_DIR_EMPTY)

    if get(Cc.IS_REMOTE):
        if _empty(Cc.SOURCE_HOST) or _empty(Cc.SOURCE_USERNAME) or _empty(Cc.SOURCE_SECRET):
            errors.append(Sc.ERR_MSG_REMOTE_CFG_EMPTY)

    # if self._empty(Const.SCHEDULE) or self._empty(Const.ACTION):
    #     errors.append(CC.ERR_MSG_SCHEDULE_ACTION_EMPTY)
    if _empty(Cc.ACTION):
        errors.append(Sc.ERR_MSG_SCHEDULE_ACTION_EMPTY)

    if not _isnone(get(Cc.EVERY)) and not _empty(Cc.AT):
        errors.append(Sc.ERR_MSG_SCHEDULE_INVALID)

    if _empty(Cc.TIME_UNIT):
        errors.append(Sc.ERR_MSG_TIME_UNIT_EMPTY)

    return errors


def _isnone(o):
    """
    check whether input is None

    Parameters
    ----------
    o : object
        any object

    Returns
    --------
    bool
        true if input is None, false otherwise

    """
    return o is None


def _empty(k):
    """
    check whether required value is missing in configurations

    Parameters
    ----------
    k : str
        a key to be searched in configurations

    Returns
    --------
    bool
        true if value not present, false otherwise

    """
    str1 = str(get(k))
    return _isnone(str1) or len(str1.strip()) == 0


def _empty_arr(arr):
    """
    checks whether input collection is empty

    Parameters
    ----------
    arr: []
        input array/collection

    Returns
    --------
    bool
        true if collection is empty, false otherwise

    """
    return _isnone(arr) or len(arr) == 0

