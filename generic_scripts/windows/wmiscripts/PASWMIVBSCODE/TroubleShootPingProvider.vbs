
Option Explicit
 
Sub Sink_OnObjectReady(oInst, oCtx)
    instcount = instCount+1
    Wscript.echo "Event " & cstr(instCount) & vbTab & _
        oInst.GetObjectText_ & vbNewLine        
End Sub
 
Sub Sink_OnCompleted(Hresult, oErr, oCtx)    
End Sub
 
'msftTroubleShooting.vbs starts here
 
DIM oLctr, oSvc, OSink, instCount, SrvName, SrvUserName, SrvPswd, args, argcount 
 
Set args = wscript.arguments
 
SrvName = "."
SrvUserName = Null
SrvPswd = Null
instcount = 0
 
argcount = args.Count
 
If (argcount > 0)  Then
    If args(0) = "/?" or args(0) = "?"   Then
        Wscript.Echo "Usage:        cscript msftTroubleShooting.vbs " _
            & "[ServerName=Null|?] [UserName=Null] [Password=Null]"
        Wscript.Echo "Example:    cscript msftTroubleShooting.vbs "
        Wscript.Echo "Example:    cscript msftTroubleShooting.vbs computerABC"
        Wscript.Echo "Example:    cscript msftTroubleShooting.vbs "
        Wscript.Echo "computerABC admin adminPswd"
        Wscript.Quit 1
    End If 
End If
 
Set oLctr = createObject("WbemScripting.Swbemlocator")
 
On Error Resume Next
If argcount = 0 Then
    Set oSvc = oLctr.ConnectServer(,"root\cimv2") 
    SrvName = " Local Computer "
Else
    srvname = args(0)
    If argcount >= 2 Then 
        SrvUserName = args(1)
    End If
    If argcount >= 3 Then 
        SrvPswd = args(2)
    End If
    Set oSvc = oLctr.ConnectServer(srvname,"root\cimv2",SrvUserName,SrvPswd)
End If
 
If Err = 0 then
    Wscript.Echo "Connection to " & srvname & " is thru"  & vbNewLine
Else
    Wscript.Echo "The Error is " & err.description & _
        " and the Error number is " & err.number
    Wscript.Quit 1
End If
 
On Error Goto 0
 
Set oSink = WScript.CreateObject("WbemScripting.SWbemSink","Sink_")
oSvc.ExecNotificationQueryAsync oSink, _
    "Select * From MSFT_WmiProvider_OperationEvent Where " & _
        "provider = 'WMIPingProvider'"
 
Wscript.Echo "To stop the script press ctrl + C" & vbNewLine
Wscript.Echo "Waiting for events......"  & vbNewLine
 
While True
    Wscript.Sleep 10000     
Wend

