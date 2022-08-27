import datetime as dt


def get_unix_timedelta(unix_time: str | dt.datetime | int):
    """Определяет дельту между текущим UNIX-временем и переданным в качестве параметра"""
    end_timestamp = unix_time
    if isinstance(unix_time, (int, str)):
        end_timestamp = dt.datetime.fromtimestamp(float(unix_time)).timestamp()

    return end_timestamp - dt.datetime.now().timestamp()
