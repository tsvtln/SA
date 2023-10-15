'==========================================================================
'
'
' COMMENT: <Use WMI eventing to watch for file creation>
'1. Looks at the cim_directoryContainsFile wmi class. Associates it With
'2. the win32_directory class. Note we use the group component which we Set
'3. equal to a directory name of c:\fso. 
'4. Uses a function to prepare the input for the win32_directory class. This 
'5. makes it easy to type in a "normal" directory name ... 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objClass 'holds wmi class to monitor
dim objGroup 
Dim StrMessage 'holds output message
Dim strFolder

strComputer = "."
wmiNS = "\root\cimv2"
objClass = "'cim_DirectoryContainsFile'"
objGroup = "'Win32_Directory.Name="
strFolder = "C:\fso"
strFolder = funFix(strFolder)
StrMessage = "A new " & objClass & " was created: "
wmiQuery = "SELECT * FROM __InstanceCreationEvent " _
        & "WITHIN 10 WHERE TargetInstance ISA " & objClass & " AND " _
            & "TargetInstance.GroupComponent= " _
                & objGroup & strFolder

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)

Do
Set objItem = colItems.NextEvent
    Wscript.Echo StrMessage & objItem.TargetInstance.PartComponent
Loop

Function funFix(strFolder)
funFix = """" & Replace(strFolder, "\", "\\\\") & """'"
End function