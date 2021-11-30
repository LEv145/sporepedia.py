from typing import Dict

from .errors import DwrParserError

from js2py import EvalJs


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

    def parse(self, text: str) -> Dict[str, str]:
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
