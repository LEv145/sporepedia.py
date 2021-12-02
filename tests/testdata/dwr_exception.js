throw 'allowScriptTagRemoting is false.';
//#DWR-REPLY
if (window.dwr) dwr.engine._remoteHandleBatchException({ name:'org.directwebremoting.extend.ServerException', message:'The specified call count is not a number' });
else if (window.parent.dwr) window.parent.dwr.engine._remoteHandleBatchException({ name:'org.directwebremoting.extend.ServerException', message:'The specified call count is not a number' });
