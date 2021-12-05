from js2py.base import (
    to_list,
    to_dict,
    Scope,
    PyJs,
    PyJsUndefined,
    PyJsNull,
    PyJsNumber,
    PyJsString,
    PyJsBoolean,
    PyObjectWrapper,
    PyJsArray,
    PyJsObject,
    JsObjectWrapper,
)
from js2py.constructors.jsdate import PyJsDate


def to_python__mockup(val):
    if not isinstance(val, PyJs):
        return val
    if isinstance(val, PyJsUndefined) or isinstance(val, PyJsNull):
        return None
    elif isinstance(val, PyJsNumber):
        # this can be either float or long/int better to assume its int/long when a whole number...
        v = val.value
        try:
            i = int(v) if v == v else v  # type: ignore
            return v if i != v else i
        except Exception:
            return v
    elif isinstance(val, (PyJsString, PyJsBoolean)):
        return val.value
    elif isinstance(val, PyObjectWrapper):
        return val.__dict__['obj']
    elif isinstance(val, PyJsArray) and val.CONVERT_TO_PY_PRIMITIVES:
        return to_list(val)
    elif isinstance(val, PyJsObject) and val.CONVERT_TO_PY_PRIMITIVES:
        return to_dict(val)
    elif isinstance(val, PyJsDate):
        return val.to_utc_dt()
    elif isinstance(val, (PyJsObject, PyJsArray, Scope)):
        return JsObjectWrapper(val)
    else:
        raise Exception(f"{type(val)} is not supported to python convert")
