import time
import configs.ConfigLoader as Cfg_Loader
import utils.StringBuilder as Sb


def current_time_in_millis() -> int:
    return int(round(time.time() * 1000))


def isnone(o) -> bool:
    return o is None


def is_empty(str1) -> bool:
    return isnone(str1) or len(str1.strip()) == 0


def is_empty_arr(arr) -> bool:
    return isnone(arr) or len(arr) == 0


def cfg(key: str):
    return Cfg_Loader.get(key)


def cfg_by_env(key: str, envp: str):
    return Cfg_Loader.get_by_env(key, envp)


def time_taken(start) -> str:
    sb = Sb.StringBuilder()
    taken = current_time_in_millis() - start
    ss = round(taken / 1000)
    sb.append(' in ')
    if ss > 0:
        sb.append(str(ss)).append(' seconds')
    else:
        sb.append(taken).append(' milliseconds')

    return sb.to_string()


def is_valid_implementation(inst, *typ) -> bool:
    return isinstance(inst, typ) and issubclass(inst.__class__, typ)


