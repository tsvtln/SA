'==========================================================================
'
'
' COMMENT: <Echos out properties of Win32_LocalTime>
'
'==========================================================================

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
wmiQuery = "win32_LocalTime=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
With objItem
	Wscript.echo "Day: "  & .Day
	Wscript.echo "DayOfWeek: "  & .DayOfWeek
	Wscript.echo "Hour: "  & .Hour
	Wscript.echo "Milliseconds: "  & .Milliseconds
	Wscript.echo "Minute: "  & .Minute
	Wscript.echo "Month: "  & .Month
	Wscript.echo "Quarter: "  & .Quarter
	Wscript.echo "Second: "  & .Second
	Wscript.echo "WeekInMonth: "  & .WeekInMonth
	Wscript.echo "Year: "  & .Year
End with