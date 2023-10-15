
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objSMTPconsumer
dim objItem

strComputer = "."
wmiNS = "\root\subscription"
wmiQuery = "smtpEventConsumer"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objSMTPconsumer = objWMIService.get(wmiQuery)
With objSMTPconsumer
	.fromLine = "edwils@microsoft.com"
	.bccLine = "ed@edwilson.net"
	.toLine = "edwils@microsoft.com"
	.ccLine = "us@edwilson.net"
	.smtpServer = "clt-msg-10.northamerica.corp.microsoft.com"
	.subject = "smtp email alert"
	.message = "test message"
	.name = "mailConsumer"	
End With


__FilterToConsumerBinding