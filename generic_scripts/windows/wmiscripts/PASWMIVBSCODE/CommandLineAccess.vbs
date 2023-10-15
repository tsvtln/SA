'==========================================================================
'
' COMMENT: <Use win32_CommandLineAccess class>
'1. returns information about command line installation. 
'2. requires the msi installer be installed on machien.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_CommandLineAccess"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo funLine("Caption:"  & objItem.Caption)
Wscript.echo "CommandLine:"  & objItem.CommandLine
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemName:"  & objItem.SystemName
Wscript.echo "Type:"  & objItem.Type
Next

'### functions below #####
Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End function