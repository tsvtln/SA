'==========================================================================
'
'
' COMMENT: <Lists running system drivers.>
'1. Use this script to find the names of systemDrivers to use use With
'2. AssociatorsOfW32SystemDrivers.vbs script. 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim vWhere
Dim intD 'The number of spaces supplied to space function.
Const intL=15 'how far over we will tab. The widest name property.
strComputer = "."
vWhere = "state = 'running'"
wmiQuery = "Select name, description from win32_systemDriver where "& Vwhere

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
With objItem
intD = funTab(Len(.name))'obtain number of spaces required for alignment
   WScript.echo  .name & ": " & Space(intD) & .description
End with
Next

'#### tab output function below 

Function funTab(funT)
Dim xfunT
xfunT = intL - funt
If xfunT<=0 Then 'catches a negative tab value
WScript.echo "******* intL Tab value should be: " & funT +1 'Tell you value for intL
funTab=1 
else
funTab=xfunT
End if
End function