'==========================================================================
'
' COMMENT: <Uses WMI Eventing>
'1. uses win32_Share and eventing to check for Modification of Share
'2. Uses dictionary to keep track of property changes
'3. Uses properties_ to enumerate all the properties of the Class
'4. Then uses value to obtain the values of the properties
'5. Then stores these in dictionary
'6. Then compares targetInstance with previousInstance.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer 'local computer
dim wmiNS 'namespace where class located
dim wmiQuery 'event driven query
dim objWMIService 'moniker connection into wmi
dim colItems 'Holds subscription to event
dim objItem 'the Event generated by Next Event
Dim objTGT 'monitored class
dim strProperty 'property associated with target instance. CURRENT
dim strPreProperty 'property associated with previous instance. OLD 
Dim objDictionary 'holds the current properties and values

strComputer = "."
objTGT = "'win32_Share'"
wmiNS = "\root\cimv2"
wmiQuery = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Set objDictionary = CreateObject("scripting.dictionary")
Do
   Set objItem = colItems.NextEvent(-1)
   WScript.Echo "share modified: " & objItem.TargetInstance.name _
    & vbtab & objItem.targetInstance.path
   subGetModifiedProperty 'adds current items to dictionary, and compares their values with previous
   
Loop

Sub subGetModifiedProperty
For Each strProperty In objItem.TargetInstance.properties_ 
   		objDictionary.add strProperty.name, strProperty.value
   next
   For Each strPreProperty In objItem.previousInstance.properties_
	if objDictionary(strPreProperty.name) <> strPreProperty.value Then
	WScript.Echo " property modified: " & strPreProperty.name 
	WScript.Echo vbtab & "Was: " & strPreProperty.value	& _
	" now: " & objDictionary(strPreProperty.name)	
   End If
   Next
   objDictionary.removeAll 'remove keys and items so can use again
End Sub 