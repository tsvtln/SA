
option explicit
dim machine

machine = "www.yahoo.com"
if reachable(machine) Then
	wscript.echo machine & " reachable"
else
	wscript.echo machine & " not reachable"
end if


function reachable(HostName)
	dim wshShell, fso, tfolder, tname, TempFile, results, retString, ts
	Const ForReading = 1, TemporaryFolder = 2
	reachable = False
	set wshShell=wscript.createobject("wscript.shell")
	set fso = CreateObject("Scripting.FileSystemObject")
	Set tfolder = fso.GetSpecialFolder(TemporaryFolder)
	tname = fso.GetTempName
	TempFile = tfolder & tname
	'-w 100000 is 5 mins worth of timeout to cope with establishing a dialup
	wshShell.run "cmd /c ping -n 3 -w 1000 " & HostName & ">" & TempFile,0,true
	set results = fso.GetFile(TempFile)
	set ts = results.OpenAsTextStream(ForReading)
	do while ts.AtEndOfStream <> True
		retString = ts.ReadLine
		if instr(retString, "Reply")>0 then
			reachable = true
			exit do
		end if
	loop
	ts.Close
	results.delete
end function
