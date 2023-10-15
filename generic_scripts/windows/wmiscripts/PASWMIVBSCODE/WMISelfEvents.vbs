'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.returns information on wmi events
'==========================================================================

strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" _
    & strComputer & "\root\CIMV2") 
Set objEvents = objWMIService.ExecNotificationQuery _
("SELECT * FROM MSFT_WmiselfEvent WITHIN 10")
Wscript.Echo "Waiting for MSFT_WmiselfEvent events"
Do While True
    Set objReceivedEvent = objEvents.NextEvent
    Wscript.Echo "Event has occurred: Event class is " _
        & objReceivedEvent.Path_.Class
Loop

