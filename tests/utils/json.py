# pragma: no cover
from contextlib import suppress
from datetime import datetime


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def json_datetime_hook(json_dict):
    for (key, value) in json_dict.items():
        with suppress(Exception):
            json_dict[key] = datetime.strptime(value, DATE_FORMAT)
    return json_dict


def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.strftime(DATE_FORMAT)
    raise TypeError("Type %s not serializable" % type(obj))
