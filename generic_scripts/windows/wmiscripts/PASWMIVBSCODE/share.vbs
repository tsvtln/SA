'==========================================================================
'
' COMMENT: <Use win32_share class>
'1. connects to a specific share, and retrieves the access permissions
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strMask
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_share where name = 'a'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "Share Name: " & objItem.name
    Wscript.Echo "Share Path: " & objItem.path
    Wscript.Echo "Share Mask Property: " & objItem.accessMask 'ALWAYS returns NULL
wscript.echo "Share Mask method:" &strAccessMask(objItem.getAccessMask)
'WScript.Echo(strMask)
Next

Function strAccessMask(inMask)
Dim strPerm
	If inMask AND 1048576 Then strPerm = strPerm & "Synchronize, "
	If inMask AND 524288 Then strPerm = strPerm & "Write Owner, "
	If inMask AND 262144 Then strPerm = strPerm & "Write DAC, "
	If inMask AND 131072 Then strPerm = strPerm & "Read Control, "
	If inMask AND 65536 Then strPerm = strPerm & "Delete, "
	If inMask AND 256 Then strPerm = strPerm & "File Write Attrib, "
	If inMask AND 128 Then strPerm = strPerm & "FIle Read Attrrib, "
	If inMask AND 64 Then strPerm = strPerm & "File Delete Child, "
	If inMask AND 32 Then strPerm = strPerm & "File Traverse, "
	If inMask AND 16 Then strPerm = strPerm & "File Write Ext Attr, "
	If inMask AND 8 Then strPerm = strPerm & "File Read Ext Attr, " 
	If inMask AND 4 Then strPerm = strPerm & "File Add Sub, "
	If inMask AND 2 Then strPerm = strPerm & "File Add File, " 
	If inMask AND 1 Then strPerm = strPerm & "File List Dir. "
strAccessMask = strPerm
End Function