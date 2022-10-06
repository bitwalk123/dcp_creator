$appname = "dcp_creator"
$mainscript = "app.py"
$icofile = "favicon.ico"
$basedir = "..\Packages"
#
$work = "build"
$dist = "dist"
$workpath = @($basedir, $work) -join "\"
$distpath = @($basedir, $dist) -join "\"
# PyInstaller
pyinstaller -w -i $icofile --workpath $workpath --distpath $distpath -n $appname $mainscript