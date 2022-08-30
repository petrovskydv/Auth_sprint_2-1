import datetime as dt
from user_agents import parse
from enum import Enum


class Device(Enum):
    WEB = 'Браузер'
    MOBILE = 'Телефон'
    SMART = 'Смарт-ТВ'


def useragent_device_parser(useragent: str) -> Device | None:
    """Считывает устройство из строки Юзер-Агента"""
    user_agent = parse(useragent)
    # Парсим устройства
    if str(user_agent).find("TV") != -1:
        return Device.SMART
    if user_agent.is_mobile or user_agent.is_tablet:
        return Device.MOBILE
    if user_agent.is_pc:
        return Device.WEB

    return None


def get_unix_timedelta(unix_time: str | dt.datetime | int):
    """Определяет дельту между текущим UNIX-временем и переданным в качестве параметра"""
    end_timestamp = unix_time
    if isinstance(unix_time, (int, str)):
        end_timestamp = dt.datetime.fromtimestamp(float(unix_time)).timestamp()

    return end_timestamp - dt.datetime.now().timestamp()
