'==========================================================================
'
'
' NAME: <AssociatorsOfNetAdaptorRequiredQualifier.vbs>
' COMMENT: <Uses an associators of query with required qualifier in the where>
'1. This script retrieves all items with localized class data associated with network card
'2. In the output section we use a trick to return the information. The trick Is
'3. That each of the associated classes DO NOT have the same properties, even name
'4. So what do we echo out. Well they all have a property path!
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
wmiQuery = "associators of {win32_networkadapter.deviceID='1'} where requiredQualifier = locale"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.execquery(wmiQuery)
For Each objItem in colItems
     Wscript.Echo objItem.path_.relpath
Next