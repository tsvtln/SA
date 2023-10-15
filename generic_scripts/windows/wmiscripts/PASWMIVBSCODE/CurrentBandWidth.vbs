'==========================================================================
'
' COMMENT: <Uses a performance formatted wmi class to determine current bandwidth>
'1. Win32_PerfFormattedData_Tcpip_NetworkInterface is the wmi Class
'2. name is a key value, and selected automatically
'3. As there is no where clause, it returns ALL the adapters
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select CurrentBandwidth from Win32_PerfFormattedData_Tcpip_NetworkInterface"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
strMSG = strMSG & vbcrlf & "Name:  " & objItem.Name & vbcrlf & _
   vbtab & "CurrentBandwidth: " & objItem.CurrentBandwidth
Next
WScript.Echo strMSG