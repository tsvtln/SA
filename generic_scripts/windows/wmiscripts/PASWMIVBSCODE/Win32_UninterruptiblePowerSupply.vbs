Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_UninterruptiblePowerSupply"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "ActiveInputVoltage: " & objItem.ActiveInputVoltage
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "BatteryInstalled: " & objItem.BatteryInstalled
 wscript.echo "CanTurnOffRemotely: " & objItem.CanTurnOffRemotely
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CommandFile: " & objItem.CommandFile
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "EstimatedChargeRemaining: " & objItem.EstimatedChargeRemaining
 wscript.echo "EstimatedRunTime: " & objItem.EstimatedRunTime
 wscript.echo "FirstMessageDelay: " & objItem.FirstMessageDelay
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "IsSwitchingSupply: " & objItem.IsSwitchingSupply
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "LowBatterySignal: " & objItem.LowBatterySignal
 wscript.echo "MessageInterval: " & objItem.MessageInterval
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerFailSignal: " & objItem.PowerFailSignal
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "Range1InputFrequencyHigh: " & objItem.Range1InputFrequencyHigh
 wscript.echo "Range1InputFrequencyLow: " & objItem.Range1InputFrequencyLow
 wscript.echo "Range1InputVoltageHigh: " & objItem.Range1InputVoltageHigh
 wscript.echo "Range1InputVoltageLow: " & objItem.Range1InputVoltageLow
 wscript.echo "Range2InputFrequencyHigh: " & objItem.Range2InputFrequencyHigh
 wscript.echo "Range2InputFrequencyLow: " & objItem.Range2InputFrequencyLow
 wscript.echo "Range2InputVoltageHigh: " & objItem.Range2InputVoltageHigh
 wscript.echo "Range2InputVoltageLow: " & objItem.Range2InputVoltageLow
 wscript.echo "RemainingCapacityStatus: " & objItem.RemainingCapacityStatus
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TimeOnBackup: " & objItem.TimeOnBackup
 wscript.echo "TotalOutputPower: " & objItem.TotalOutputPower
 wscript.echo "TypeOfRangeSwitching: " & objItem.TypeOfRangeSwitching
 wscript.echo "UPSPort: " & objItem.UPSPort
wscript.echo " "
next
