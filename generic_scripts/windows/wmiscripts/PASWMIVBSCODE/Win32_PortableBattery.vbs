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
wmiQuery = "Select * from Win32_PortableBattery"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "BatteryStatus: " & objItem.BatteryStatus
 wscript.echo "CapacityMultiplier: " & objItem.CapacityMultiplier
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Chemistry: " & objItem.Chemistry
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DesignCapacity: " & objItem.DesignCapacity
 wscript.echo "DesignVoltage: " & objItem.DesignVoltage
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "EstimatedChargeRemaining: " & objItem.EstimatedChargeRemaining
 wscript.echo "EstimatedRunTime: " & objItem.EstimatedRunTime
 wscript.echo "ExpectedLife: " & objItem.ExpectedLife
 wscript.echo "FullChargeCapacity: " & objItem.FullChargeCapacity
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Location: " & objItem.Location
 wscript.echo "ManufactureDate: " & objItem.ManufactureDate
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MaxBatteryError: " & objItem.MaxBatteryError
 wscript.echo "MaxRechargeTime: " & objItem.MaxRechargeTime
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "SmartBatteryVersion: " & objItem.SmartBatteryVersion
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TimeOnBattery: " & objItem.TimeOnBattery
 wscript.echo "TimeToFullCharge: " & objItem.TimeToFullCharge
wscript.echo " "
Next