Function CurrentPath()
    strPath = Wscript.ScriptFullName
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(strPath)
    CurrentPath = objFSO.GetParentFolderName(objFile)
End Function

strCurrentPath = CurrentPath()
quo = """"

strArgs = quo & strCurrentPath & "\code\default\python27\1.0\python.exe" & quo & " " & quo & strCurrentPath & "\code\default\launcher\start.py" & quo

Set oShell = CreateObject ("Wscript.Shell")
oShell.Run strArgs, 0