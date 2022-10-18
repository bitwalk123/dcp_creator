$appname = "dcp_creator"
$specfile = $appname + ".spec"
$mainscript = "app.py"
$icofile = "favicon.ico"
$basedir = "..\Packages"
$verfile = "version.txt"
#
$work = "build"
$dist = "dist"
$workpath = @($basedir, $work) -join "\"
$distpath = @($basedir, $dist) -join "\"
# delete old workspace just in case
if (Test-Path $verfile) {
    Remove-Item -Path $verfile -Force
}
if (Test-Path $specfile) {
    Remove-Item -Path $specfile -Force
}
if (Test-Path $workpath) {
    Remove-Item -Path $workpath -Recurse -Force
}
if (Test-Path $distpath) {
    Remove-Item -Path $distpath -Recurse -Force
}
# Generate Version Info
python gen_version_file.py
# PyInstaller
pyinstaller -w -i $icofile --version-file $verfile --workpath $workpath --distpath $distpath -n $appname $mainscript