# If you're not an admin, you might want to use this to set your paths so you can
# open PowerShell with this link and have your environment all set up for you. 

# Path to LasTools binaries
$env:PATH += ";C:\lastools\bin"


# Path to ArcGIS's version of Python
$env:PATH += ";C:\Python27\ArcGIS10.2"

# This determine the path to the directory where this script is located
$fullPathIncFileName = $MyInvocation.MyCommand.Definition
$currentScriptName = $MyInvocation.MyCommand.Name
$currentExecutingPath = $fullPathIncFileName.Replace($currentScriptName, "")

# Add the path to the solar_scripts to PATH and PYTHONPATH
$env:PATH += ";" + $currentExecutingPath
$env:PYTHONPATH += ";" + $currentExecutingPath


# Set other paths here. settings that might be usefull, like Git and Vim
$env:PATH += ";C:\Users\moor1090\AppData\Local\GitHub\PortableGit_054f2e797ebafd44a30203088cd3d58663c627ef\bin"
$env:PATH += ";C:\Users\moor1090\AppData\Local\GitHub\PortableGit_054f2e797ebafd44a30203088cd3d58663c627ef\cmd"
$env:PATH += ";C:\Users\moor1090\gVimPortable\App\vim\vim74" 

