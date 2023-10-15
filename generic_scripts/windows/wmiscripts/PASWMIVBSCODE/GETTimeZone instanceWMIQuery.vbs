strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_TimeZone",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_TimeZone instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Bias: " & objItem.Bias
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "DaylightBias: " & objItem.DaylightBias
    Wscript.Echo "DaylightDay: " & objItem.DaylightDay
    Wscript.Echo "DaylightDayOfWeek: " & objItem.DaylightDayOfWeek
    Wscript.Echo "DaylightHour: " & objItem.DaylightHour
    Wscript.Echo "DaylightMillisecond: " & objItem.DaylightMillisecond
    Wscript.Echo "DaylightMinute: " & objItem.DaylightMinute
    Wscript.Echo "DaylightMonth: " & objItem.DaylightMonth
    Wscript.Echo "DaylightName: " & objItem.DaylightName
    Wscript.Echo "DaylightSecond: " & objItem.DaylightSecond
    Wscript.Echo "DaylightYear: " & objItem.DaylightYear
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "SettingID: " & objItem.SettingID
    Wscript.Echo "StandardBias: " & objItem.StandardBias
    Wscript.Echo "StandardDay: " & objItem.StandardDay
    Wscript.Echo "StandardDayOfWeek: " & objItem.StandardDayOfWeek
    Wscript.Echo "StandardHour: " & objItem.StandardHour
    Wscript.Echo "StandardMillisecond: " & objItem.StandardMillisecond
    Wscript.Echo "StandardMinute: " & objItem.StandardMinute
    Wscript.Echo "StandardMonth: " & objItem.StandardMonth
    Wscript.Echo "StandardName: " & objItem.StandardName
    Wscript.Echo "StandardSecond: " & objItem.StandardSecond
    Wscript.Echo "StandardYear: " & objItem.StandardYear
Next