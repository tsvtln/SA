'==========================================================================
' COMMENT: <Uses an associators query for logical Disk>
'1. returns associations of the win32_logicalDisk
'2. uses an associators of type of query
'3. curley brackets {} are required for this query
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strClass

strComputer = "."
strClass = "{win32_logicalDisk.deviceID='c:'}"
wmiNS = "\root\cimv2"
wmiQuery = "ASSOCIATORS OF " & strClass
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery (wmiQuery)


 For Each objItem in colItems
     Wscript.Echo "Path_ = " & objItem.path_
     WScript.Echo vbtab & " relPath = " & objItem.path_.relpath

 Next