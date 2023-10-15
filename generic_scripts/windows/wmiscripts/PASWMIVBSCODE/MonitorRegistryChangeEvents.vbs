'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Does an execNotificationQueryAsync query and therefore has to use a
'2.SwbemSink. It is a simple createobject command, but you specify the sink_
'3. 
'==========================================================================
Option Explicit
'On Error Resume next
Dim strEvent 'holds name of event
Dim strHive 'holds Registry Hive
Dim strKeyPath 'holds the key path. Note: only need a single "\" between keys
Dim objWMIServices 'holds connection into WMI using the Moniker
Dim objWMISink 'creates the wbemScripting Sink. MUST use wscript in front of CreateObject command!
strEvent = "SELECT * FROM RegistryKeyChangeEvent"
strHive = "HKEY_LOCAL_MACHINE"
strKeyPath = "SOFTWARE\Microsoft\Windows NT\CurrentVersion"

Set objWmiServices = GetObject("winmgmts:root/default") 
Set objWmiSink = Wscript.createObject("WbemScripting.SWbemSink", "SINK_") 

objWmiServices.ExecNotificationQueryAsync objWmiSink, _ 
    funMakeStr(strEvent,strHive,StrKeyPath)
'WScript.Echo funMakeStr(strEvent,strHive,StrKeyPath) 'debug
WScript.Echo "Monitoring for Registry Changes ..." & vbCrLf 

While(true) 
    WScript.Sleep 2000 
Wend 

Sub SINK_OnObjectReady(wmiObject, wmiAsyncContext) 
    WScript.Echo "Registry Change occurred" & vbCrLf & _ 
                 "------------------------------" & vbCrLf & _ 
                 wmiObject.GetObjectText_() 
End Sub

' ### The two functions below fix up the execNotificationQuery string. They allow the
'     entry of cleaner strings in the three strings used to hold all the parameters For
'     the command. ###
Function funMakeStr(strEvent,strHive,strKeyPath)
funMakeStr = strEvent & " Where Hive ='" & strHive & "'"& _
	"And keyPath=" & funFixKeyPath(strKeyPath)
End Function

Function funFixKeyPath(strKeyPath)
funFixKeyPath = "'" & replace(strKeyPath,"\","\\") & "'"
End function