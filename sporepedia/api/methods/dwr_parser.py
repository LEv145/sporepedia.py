from typing import Any
from unittest.mock import patch

import js2py
from js2py import EvalJs
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


def parse_dwr(raw_data: str) -> JsObjectWrapper:
    parser = SporeDwrEngineParser()
    return parser.parse(raw_data)


class SporeDwrEngineParser():
    _extension_code = (
        "outlog = null;\n"
        "errorlog = null;\n"

        "dwr = {};\n"
        "dwr.engine = {};\n"

        "dwr.engine._remoteHandleBatchException = function(exeption, batchId) {\n"
        "    errorlog = exeption;\n"
        "};\n"

        "dwr.engine._remoteHandleCallback = function(batchId, callId, reply) {\n"
        "    outlog = reply;\n"
        "};\n"
    )

    def parse(self, raw_data: str) -> "JsObjectWrapper":
        js_code = raw_data.replace("throw 'allowScriptTagRemoting is false.';", "")  # Remove throw

        context = EvalJs()
        context.execute(
            (
                f"{self._extension_code}"
                f"{js_code}"
            )
        )

        patcher = patch.object(
            js2py.base,
            "to_python",
            to_python__mockup,
        )
        patcher.start()

        outlog, errorlog = context.outlog, context.errorlog

        if errorlog is not None:
            raise DwrParserError(message=errorlog["message"], name=errorlog["name"])

        return outlog


class DwrParserError(Exception):
    def __init__(self, message: str, name: str) -> None:
        super().__init__()
        self.message = message
        self.name = name


def to_python__mockup(val: Any) -> Any:
    if not isinstance(val, PyJs):  # pragma: no cover
        return val
    if isinstance(val, PyJsUndefined) or isinstance(val, PyJsNull):  # pragma: no cover
        return None
    elif isinstance(val, PyJsNumber):  # pragma: no cover
        # this can be either float or long/int better to assume its int/long when a whole number...
        v = val.value
        try:
            i = int(v) if v == v else v  # type: ignore
            return v if i != v else i
        except Exception:
            return v
    elif isinstance(val, (PyJsString, PyJsBoolean)):  # pragma: no cover
        return val.value
    elif isinstance(val, PyObjectWrapper):  # pragma: no cover
        return val.__dict__['obj']
    elif isinstance(val, PyJsArray) and val.CONVERT_TO_PY_PRIMITIVES:  # pragma: no cover
        return to_list(val)
    elif isinstance(val, PyJsObject) and val.CONVERT_TO_PY_PRIMITIVES:  # pragma: no cover
        return to_dict(val)
    elif isinstance(val, PyJsDate):
        return val.to_utc_dt()
    elif isinstance(val, (PyJsObject, PyJsArray, Scope)):
        return JsObjectWrapper(val)
    else:  # pragma: no cover
        raise Exception(f"{type(val)} is not supported to python convert")
