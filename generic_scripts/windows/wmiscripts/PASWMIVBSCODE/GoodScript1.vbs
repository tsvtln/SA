'==========================================================================
'
'
' COMMENT: <This is a good script that does work.>
'1. This script is used in lab 28 of chapter 14.  
'2. It will generate events in the log files. That is the point of the lab!
'3. It is not a super exciting script, but it does return info about your CPU.
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strOUT

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_Processor"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    strOUT = strOUT & vbcrlf & "name: " & objItem.name
    strOUT = strOUT & vbcrlf & "AddressWidth: " & objItem.AddressWidth
    strOUT = strOUT & vbcrlf & "Architecture: " & objItem.Architecture 
    strOUT = strOUT & vbcrlf & "Manufacturer: " & objItem.Manufacturer 
    strOUT = strOUT & vbcrlf & "MaxClockSpeed: " & objItem.MaxClockSpeed 
Next

strOUT = strOUT & vbcrlf & "This script ran successfully. " & Now
WScript.Echo(strOUT)
