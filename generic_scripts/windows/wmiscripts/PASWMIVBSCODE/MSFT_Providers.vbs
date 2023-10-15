'==========================================================================
'
'
' COMMENT: <Uses MSFT_Providers class to report on provider health and operation.>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from MSFT_Providers"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "HostingGroup:"  & objItem.HostingGroup
Wscript.echo "HostingSpecification:"  & objItem.HostingSpecification
Wscript.echo "HostProcessIdentifier:"  & objItem.HostProcessIdentifier
Wscript.echo "Locale:"  & objItem.Locale
Wscript.echo "Namespace:"  & objItem.Namespace
Wscript.echo "provider:"  & objItem.provider
Wscript.echo "ProviderOperation_AccessCheck:"  & cdbl(objItem.ProviderOperation_AccessCheck)
Wscript.echo "ProviderOperation_CancelQuery:"  & cdbl(objItem.ProviderOperation_CancelQuery)
Wscript.echo "ProviderOperation_CreateClassEnumAsync:"  & cdbl(objItem.ProviderOperation_CreateClassEnumAsync)
Wscript.echo "ProviderOperation_CreateInstanceEnumAsync:"  & cdbl(objItem.ProviderOperation_CreateInstanceEnumAsync)
Wscript.echo "ProviderOperation_CreateRefreshableEnum:"  & cdbl(objItem.ProviderOperation_CreateRefreshableEnum)
Wscript.echo "ProviderOperation_CreateRefreshableObject:"  & cdbl(objItem.ProviderOperation_CreateRefreshableObject)
Wscript.echo "ProviderOperation_CreateRefresher:"  & cdbl(objItem.ProviderOperation_CreateRefresher)
Wscript.echo "ProviderOperation_DeleteClassAsync:"  & cdbl(objItem.ProviderOperation_DeleteClassAsync)
Wscript.echo "ProviderOperation_DeleteInstanceAsync:"  & cdbl(objItem.ProviderOperation_DeleteInstanceAsync)
Wscript.echo "ProviderOperation_ExecMethodAsync:"  & cdbl(objItem.ProviderOperation_ExecMethodAsync)
Wscript.echo "ProviderOperation_ExecQueryAsync:"  & cdbl(objItem.ProviderOperation_ExecQueryAsync)
Wscript.echo "ProviderOperation_FindConsumer:"  & cdbl(objItem.ProviderOperation_FindConsumer)
Wscript.echo "ProviderOperation_GetObjectAsync:"  & cdbl(objItem.ProviderOperation_GetObjectAsync)
Wscript.echo "ProviderOperation_GetObjects:"  & cdbl(objItem.ProviderOperation_GetObjects)
Wscript.echo "ProviderOperation_GetProperty:"  & cdbl(objItem.ProviderOperation_GetProperty)
Wscript.echo "ProviderOperation_NewQuery:"  & cdbl(objItem.ProviderOperation_NewQuery)
Wscript.echo "ProviderOperation_ProvideEvents:"  & cdbl(objItem.ProviderOperation_ProvideEvents)
Wscript.echo "ProviderOperation_PutClassAsync:"  & cdbl(objItem.ProviderOperation_PutClassAsync)
Wscript.echo "ProviderOperation_PutInstanceAsync:"  & cdbl(objItem.ProviderOperation_PutInstanceAsync)
Wscript.echo "ProviderOperation_PutProperty:"  & cdbl(objItem.ProviderOperation_PutProperty)
Wscript.echo "ProviderOperation_QueryInstances:"  & cdbl(objItem.ProviderOperation_QueryInstances)
Wscript.echo "ProviderOperation_SetRegistrationObject:"  & cdbl(objItem.ProviderOperation_SetRegistrationObject)
Wscript.echo "ProviderOperation_StopRefreshing:"  & cdbl(objItem.ProviderOperation_StopRefreshing)
Wscript.echo "ProviderOperation_ValidateSubscription:"  & cdbl(objItem.ProviderOperation_ValidateSubscription)
Wscript.echo "TransactionIdentifier:"  & objItem.TransactionIdentifier
Wscript.echo "User:"  & objItem.User
Next