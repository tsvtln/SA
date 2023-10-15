'==========================================================================
'
' COMMENT: <Use win32_ShortCutAction class>
'1. displays every shortcut on system created via MSI. 
'
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
wmiQuery = "Select * from win32_ShortCutAction"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo funLine("ActionID:"  & objItem.ActionID)
Wscript.echo "Arguments:"  & objItem.Arguments
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "Direction:"  & objItem.Direction
Wscript.echo "HotKey:"  & objItem.HotKey
Wscript.echo "IconIndex:"  & objItem.IconIndex
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "Shortcut:"  & objItem.Shortcut
Wscript.echo "ShowCmd:"  & objItem.ShowCmd
Wscript.echo "SoftwareElementID:"  & objItem.SoftwareElementID
Wscript.echo "SoftwareElementState:"  & objItem.SoftwareElementState
Wscript.echo "Target:"  & objItem.Target
Wscript.echo "TargetOperatingSystem:"  & objItem.TargetOperatingSystem
Wscript.echo "Version:"  & objItem.Version
Wscript.echo "WkDir:"  & objItem.WkDir
Next


'### functions below ###
Function funLine(lineOfText)
Dim numEQs, separator, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separator = separator & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End function