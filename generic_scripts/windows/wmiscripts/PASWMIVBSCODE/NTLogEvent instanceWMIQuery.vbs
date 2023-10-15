strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_NTLogEvent",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_NTLogEvent instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Category: " & objItem.Category
    Wscript.Echo "CategoryString: " & objItem.CategoryString
    Wscript.Echo "ComputerName: " & objItem.ComputerName
    If isNull(objItem.Data) Then
        Wscript.Echo "Data: "
    Else
        Wscript.Echo "Data: " & Join(objItem.Data, ",")
    End If
    Wscript.Echo "EventCode: " & objItem.EventCode
    Wscript.Echo "EventIdentifier: " & objItem.EventIdentifier
    Wscript.Echo "EventType: " & objItem.EventType
    If isNull(objItem.InsertionStrings) Then
        Wscript.Echo "InsertionStrings: "
    Else
        Wscript.Echo "InsertionStrings: " & Join(objItem.InsertionStrings, ",")
    End If
    Wscript.Echo "Logfile: " & objItem.Logfile
    Wscript.Echo "Message: " & objItem.Message
    Wscript.Echo "RecordNumber: " & objItem.RecordNumber
    Wscript.Echo "SourceName: " & objItem.SourceName
    Wscript.Echo "TimeGenerated: " & objItem.TimeGenerated
    Wscript.Echo "TimeWritten: " & objItem.TimeWritten
    Wscript.Echo "Type: " & objItem.Type
    Wscript.Echo "User: " & objItem.User
Next