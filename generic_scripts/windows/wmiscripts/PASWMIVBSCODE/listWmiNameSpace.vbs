'==========================================================================
'
' COMMENT: <Makes a connection to winmgmts
' uses objSwbemServices to look for instances of namespace
' uses a for each next loop to echo the results.>
'
'==========================================================================

strComputer = "."

Set objSWbemServices = GetObject("winmgmts:\\" & strComputer & "\root")
Set colNameSpaces = objSwbemServices.InstancesOf("__NAMESPACE")

For Each objNameSpace In colNameSpaces
    Wscript.Echo objNameSpace.Name
Next
