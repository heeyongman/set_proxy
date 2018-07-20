Function CurrentPath()
    strPath = Wscript.ScriptFullName
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(strPath)
    CurrentPath = objFSO.GetParentFolderName(objFile)
End Function

strCurrentPath = CurrentPath()
cmd_line = strCurrentPath & "\..\python27\1.0\python.exe " & strCurrentPath & "\set_proxy.py"

Set ws = CreateObject("wscript.shell")
ws.run cmd_line,0,false