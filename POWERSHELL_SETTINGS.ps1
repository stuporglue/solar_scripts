# If you're not an admin, you might want to use this to set your paths so you can
# open PowerShell with this link and have your environment all set up for you. 

# This determine the path to the directory where this script is located
$currentExecutingPath = $MyInvocation.MyCommand.Definition.Replace($MyInvocation.MyCommand.Name, "")

# Path to ArcGIS's version of Python
# Make our directry first, then our python
$env:PATH = $currentExecutingPath + ";C:\Python27\ArcGISx6410.2;" + $env:PATH

$env:PYTHONPATH = $currentExecutingPath + ";" + $env:PYTHONPATH
