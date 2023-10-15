
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_BaseBoard"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ConfigOptions:"  & join(objItem.ConfigOptions)
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "Depth:"  & objItem.Depth
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "Height:"  & objItem.Height
Wscript.echo "HostingBoard:"  & objItem.HostingBoard
Wscript.echo "HotSwappable:"  & objItem.HotSwappable
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "Manufacturer:"  & objItem.Manufacturer
Wscript.echo "Model:"  & objItem.Model
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "OtherIdentifyingInfo:"  & objItem.OtherIdentifyingInfo
Wscript.echo "PartNumber:"  & objItem.PartNumber
Wscript.echo "PoweredOn:"  & objItem.PoweredOn
Wscript.echo "Product:"  & objItem.Product
Wscript.echo "Removable:"  & objItem.Removable
Wscript.echo "Replaceable:"  & objItem.Replaceable
Wscript.echo "RequirementsDescription:"  & objItem.RequirementsDescription
Wscript.echo "RequiresDaughterBoard:"  & objItem.RequiresDaughterBoard
Wscript.echo "SerialNumber:"  & objItem.SerialNumber
Wscript.echo "SKU:"  & objItem.SKU
Wscript.echo "SlotLayout:"  & objItem.SlotLayout
Wscript.echo "SpecialRequirements:"  & objItem.SpecialRequirements
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "Tag:"  & objItem.Tag
Wscript.echo "Version:"  & objItem.Version
Wscript.echo "Weight:"  & objItem.Weight
Wscript.echo "Width:"  & objItem.Width
Next