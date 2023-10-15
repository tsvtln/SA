'==========================================================================
'
'
' NAME: <BadScript1.vbs>
' COMMENT: <This is a bad script that does not WORK!!!!!>
'1. This script is used in lab 28 of chapter 14. IT DOES NOT WORK. 
'2. It will generate errors in the log files. That is the point of the lab!
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv1"
wmiQuery = "Select * from win32_Processer"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo ": " & objItem.name
    Wscript.Echo ": " & objItem.bandwidth
    Wscript.Echo ": " & objItem.archetecture
    Wscript.Echo ": " & objItem.make
    Wscript.Echo ": " & objItem.model
    Wscript.Echo ": " & objItem.somethingelse
Next

WScript.Echo "This script ran successfully. " & NOW