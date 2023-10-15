'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Creates a new WMI NameSpace using VBScript
'2.Use get to get an instance of __Namespace
'3. Then have to spawn a new instance of the __Namespace Class
'4. We then assign a name to the namespace
'5. Finally, we put the instance into WMI. 
'==========================================================================

strComputer = "."
Set objSWbemServices = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root")

Set objConsumerClass = objSWbemServices.Get("__Namespace")
Set objConsumer = objConsumerClass.SpawnInstance_()
objConsumer.name = "MyNS"

objConsumer.Put_()

