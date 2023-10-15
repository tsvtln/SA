'==========================================================================
'
'
' COMMENT: <Uses the __CIMOMIdentification class to display versioning info>
'1. this class resides in TWO namespaces: root and root\default
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim strOut

strComputer = "."
wmiNS = "\root\default"
wmiQuery = "__CIMOMIdentification=@"'only one instance of cimom. Found @ instance in wbemtest
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

With objItem
    strOut = "setupTime: " & .setupTime 
    strOut = strOut & vbcrlf &"setupDate: " & .setupDate
    strOut = strOut & vbcrlf &"VersionCurrentlyRunning: " & .VersionCurrentlyRunning
    strOut = strOut & vbcrlf &"versionUsedToCreateDB: " & .versionUsedToCreateDB
    strOut = strOut & vbcrlf &"WorkingDirectory: " & .WorkingDirectory
end With

WScript.echo strOut