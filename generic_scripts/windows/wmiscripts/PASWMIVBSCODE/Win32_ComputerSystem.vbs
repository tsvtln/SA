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
wmiQuery = "Select * from Win32_ComputerSystem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AdminPasswordStatus: " & objItem.AdminPasswordStatus
 wscript.echo "AutomaticResetBootOption: " & objItem.AutomaticResetBootOption
 wscript.echo "AutomaticResetCapability: " & objItem.AutomaticResetCapability
 wscript.echo "BootOptionOnLimit: " & objItem.BootOptionOnLimit
 wscript.echo "BootOptionOnWatchDog: " & objItem.BootOptionOnWatchDog
 wscript.echo "BootROMSupported: " & objItem.BootROMSupported
 wscript.echo "BootupState: " & objItem.BootupState
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ChassisBootupState: " & objItem.ChassisBootupState
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "CurrentTimeZone: " & objItem.CurrentTimeZone
 wscript.echo "DaylightInEffect: " & objItem.DaylightInEffect
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Domain: " & objItem.Domain
 wscript.echo "DomainRole: " & objItem.DomainRole
 wscript.echo "EnableDaylightSavingsTime: " & objItem.EnableDaylightSavingsTime
 wscript.echo "FrontPanelResetStatus: " & objItem.FrontPanelResetStatus
 wscript.echo "InfraredSupported: " & objItem.InfraredSupported
 wscript.echo "InitialLoadInfo: " & objItem.InitialLoadInfo
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "KeyboardPasswordStatus: " & objItem.KeyboardPasswordStatus
 wscript.echo "LastLoadInfo: " & objItem.LastLoadInfo
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "Model: " & objItem.Model
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NameFormat: " & objItem.NameFormat
 wscript.echo "NetworkServerModeEnabled: " & objItem.NetworkServerModeEnabled
 wscript.echo "NumberOfProcessors: " & objItem.NumberOfProcessors
 wscript.echo "OEMLogoBitmap: " & objItem.OEMLogoBitmap
 wscript.echo "OEMStringArray: " & objItem.OEMStringArray
 wscript.echo "PartOfDomain: " & objItem.PartOfDomain
 wscript.echo "PauseAfterReset: " & objItem.PauseAfterReset
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "PowerOnPasswordStatus: " & objItem.PowerOnPasswordStatus
 wscript.echo "PowerState: " & objItem.PowerState
 wscript.echo "PowerSupplyState: " & objItem.PowerSupplyState
 wscript.echo "PrimaryOwnerContact: " & objItem.PrimaryOwnerContact
 wscript.echo "PrimaryOwnerName: " & objItem.PrimaryOwnerName
 wscript.echo "ResetCapability: " & objItem.ResetCapability
 wscript.echo "ResetCount: " & objItem.ResetCount
 wscript.echo "ResetLimit: " & objItem.ResetLimit
 wscript.echo "Roles: " & objItem.Roles
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SupportContactDescription: " & objItem.SupportContactDescription
 wscript.echo "SystemStartupDelay: " & objItem.SystemStartupDelay
 wscript.echo "SystemStartupOptions: " & objItem.SystemStartupOptions
 wscript.echo "SystemStartupSetting: " & objItem.SystemStartupSetting
 wscript.echo "SystemType: " & objItem.SystemType
 wscript.echo "ThermalState: " & objItem.ThermalState
 wscript.echo "TotalPhysicalMemory: " & objItem.TotalPhysicalMemory
 wscript.echo "UserName: " & objItem.UserName
 wscript.echo "WakeUpType: " & objItem.WakeUpType
 wscript.echo "Workgroup: " & objItem.Workgroup
wscript.echo " "
next
