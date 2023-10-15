strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_LocalTime",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_LocalTime instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Day: " & objItem.Day
    Wscript.Echo "DayOfWeek: " & objItem.DayOfWeek
    Wscript.Echo "Hour: " & objItem.Hour
    Wscript.Echo "Milliseconds: " & objItem.Milliseconds
    Wscript.Echo "Minute: " & objItem.Minute
    Wscript.Echo "Month: " & objItem.Month
    Wscript.Echo "Quarter: " & objItem.Quarter
    Wscript.Echo "Second: " & objItem.Second
    Wscript.Echo "WeekInMonth: " & objItem.WeekInMonth
    Wscript.Echo "Year: " & objItem.Year
Next