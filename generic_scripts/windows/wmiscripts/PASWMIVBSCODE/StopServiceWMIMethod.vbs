
strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
' Obtain an instance of the the class 
' using a key property value.
Set objShare = objWMIService.Get("Win32_Service.Name='Alerter'")

' no InParameters to define

' Execute the method and obtain the return status.
' The OutParameters object in objOutParams
' is created by the provider.
Set objOutParams = objWMIService.ExecMethod("Win32_Service.Name='Alerter'", "StopService")

' List OutParams
Wscript.Echo "Out Parameters: "
Wscript.echo "ReturnValue: " & objOutParams.ReturnValue
