from typing import TYPE_CHECKING

from .errors import DwrParserError

from js2py import EvalJs

if TYPE_CHECKING:
    from js2py.base import JsObjectWrapper


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

    def parse(self, text: str) -> "JsObjectWrapper":
        js_code = text.replace("throw 'allowScriptTagRemoting is false.';", "")  # Remove throw

        context = EvalJs()

        context.execute(
            (
                f"{self._extension_code}"
                f"{js_code}"
            )
        )

        outlog, errorlog = context.outlog, context.errorlog

        if errorlog is not None:
            raise DwrParserError(message=errorlog["message"], name=errorlog["name"])

        return outlog
