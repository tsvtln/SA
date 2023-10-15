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
wmiQuery = "Select * from Win32_Battery"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems:With objItem
 wscript.echo "Availability: " & .Availability
 wscript.echo "BatteryStatus: " & .BatteryStatus
 wscript.echo "Caption: " & .Caption
 wscript.echo "Chemistry: " & .Chemistry
 wscript.echo "ConfigManagerErrorCode: " & .ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & .ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & .CreationClassName
 wscript.echo "Description: " & .Description
 wscript.echo "DesignCapacity: " & .DesignCapacity
 wscript.echo "DesignVoltage: " & .DesignVoltage/1000'reports in millivolts
 wscript.echo "DeviceID: " & .DeviceID
 wscript.echo "ErrorCleared: " & .ErrorCleared
 wscript.echo "ErrorDescription: " & .ErrorDescription
 wscript.echo "EstimatedChargeRemaining: " & .EstimatedChargeRemaining
 wscript.echo "EstimatedRunTime: " & .EstimatedRunTime/60'reports in minutes
 wscript.echo "ExpectedLife: " & .ExpectedLife
 wscript.echo "FullChargeCapacity: " & .FullChargeCapacity
 wscript.echo "InstallDate: " & .InstallDate
 wscript.echo "LastErrorCode: " & .LastErrorCode
 wscript.echo "MaxRechargeTime: " & .MaxRechargeTime
 wscript.echo "Name: " & .Name
 wscript.echo "PNPDeviceID: " & .PNPDeviceID
 If not IsNull(.PowerManagementCapabilities)then
 wscript.echo "PowerManagementCapabilities: " & Join(.PowerManagementCapabilities)
 End if
 wscript.echo "PowerManagementSupported: " & .PowerManagementSupported
 wscript.echo "SmartBatteryVersion: " & .SmartBatteryVersion
 wscript.echo "Status: " & .Status
 wscript.echo "StatusInfo: " & .StatusInfo
 wscript.echo "SystemCreationClassName: " & .SystemCreationClassName
 wscript.echo "SystemName: " & .SystemName
 wscript.echo "TimeOnBattery: " & .TimeOnBattery
 wscript.echo "TimeToFullCharge: " & .TimeToFullCharge & vbcrlf
end with:next
