
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
strComputer = "Acapulco"
wmiNS = "\root\wmi"
wmiQuery = "Select * from MSAcpi_ThermalZoneTemperature"

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
With objItem
 wscript.echo "Active: " & .Active
 wscript.echo "ActiveTripPoint: " & join(.ActiveTripPoint, ",")
 wscript.echo "ActiveTripPointCount: " & .ActiveTripPointCount
 wscript.echo "CriticalTripPoint: " & .CriticalTripPoint
 wscript.echo "CurrentTemperature: " & .CurrentTemperature
 wscript.echo "InstanceName: " & .InstanceName
 wscript.echo "PassiveTripPoint: " & .PassiveTripPoint
 wscript.echo "Reserved: " & .Reserved
 wscript.echo "SamplingPeriod: " & .SamplingPeriod
 wscript.echo "ThermalConstant1: " & .ThermalConstant1
 wscript.echo "ThermalConstant2: " & .ThermalConstant2
 wscript.echo "ThermalStamp: " & .ThermalStamp
wscript.echo " "
End With 
Next