
function CreateShortcut()
{
   wsh = new ActiveXObject('WScript.Shell');
   target_path = '"' + wsh.CurrentDirectory + '\\start.vbs"';
   icon_path = wsh.CurrentDirectory + '\\icon\\favicon-mac.ico';


   link = wsh.CreateShortcut(wsh.SpecialFolders("Desktop") + '\\GetProxy.lnk');
   link.TargetPath = target_path;
   link.Arguments = '';
   link.WindowStyle = 7;
   link.IconLocation = icon_path;
   link.Description = 'GetProxy';
   link.WorkingDirectory = wsh.CurrentDirectory;
   link.Save();
}


function main(){
    CreateShortcut();
}
main();
