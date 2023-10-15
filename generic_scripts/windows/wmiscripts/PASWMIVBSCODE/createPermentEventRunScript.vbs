
strcomputer = "mred" 'name of target computer. Can not use "."
wmiNS = "\root\subscription"
eClass = "__instanceModificationEvent" 'type of event to obtain
tClass = "'win32_service'" 'wmi class to monitor
tName = "'Schedule'" 'name property of target class
qQuery ="select * from " & eClass & " within 10 where targetInstance isa "_
	& tClass & " and  targetinstance.name=" & tName
set objActiveScriptConsumer=getobject("winmgmts:\\" & strcomputer & wmiNS)

'Create the event filter
set objfilterclass=objActiveScriptConsumer.get("__EventFilter")
set objfilter=objfilterclass.spawninstance_()
objfilter.name="win32ServiceModification"
objfilter.querylanguage="wql"
objfilter.query=(qQuery)
set filterpath = objfilter.put_

'Create the active script consumer
set  objConsumerClass=objActiveScriptConsumer.get("ActiveScriptEventConsumer")
set objconsumer=objconsumerclass.spawninstance_()
objconsumer.name="ToggleAlerter"
objconsumer.scriptfilename="c:\a\ToggleAlerterService.vbs"
objconsumer.scriptingengine="vbscript"
set consumerpath = objconsumer.put_

'Do the binding
FTCB = "__filterToConsumerBinding"
set objbindingclass=objActiveScriptConsumer.get(FTCB)
set objbinding=objbindingclass.spawninstance_()
objbinding.filter=filterPath
objbinding.consumer=consumerpath
objbinding.put_