'==========================================================================
'
' COMMENT: This function uses the SWbemDateTime object to convert Time:
'1.Takes an WMI time format, and converts it.
'==========================================================================

Function FunTime(wmiTime)
 Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function