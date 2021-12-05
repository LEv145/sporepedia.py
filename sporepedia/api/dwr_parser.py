from js2py.base import JsObjectWrapper
from js2py import EvalJs


def parse_dwr(raw_data: str):
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

        outlog, errorlog = context.outlog, context.errorlog

        if errorlog is not None:
            raise DwrParserError(message=errorlog["message"], name=errorlog["name"])

        return outlog


class DwrParserError(Exception):
    def __init__(self, message: str, name: str) -> None:
        self.message = message
        self.name = name
