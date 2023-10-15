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
wmiQuery = "Select * from Win32_PrinterController"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AccessState: " & objItem.AccessState
 wscript.echo "Antecedent: " & objItem.Antecedent
 wscript.echo "Dependent: " & objItem.Dependent
 wscript.echo "NegotiatedDataWidth: " & objItem.NegotiatedDataWidth
 wscript.echo "NegotiatedSpeed: " & objItem.NegotiatedSpeed
 wscript.echo "NumberOfHardResets: " & objItem.NumberOfHardResets
 wscript.echo "NumberOfSoftResets: " & objItem.NumberOfSoftResets
wscript.echo " "
next
