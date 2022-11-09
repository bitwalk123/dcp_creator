$appname = "dcp_creator"
$verfile = "version.txt"
$specfile = $appname + ".spec"
$mainscript = "app.py"
$currentdir = Get-Location
$icofile = @($currentdir, "image", "favicon.ico") -join "\"
#
$work = "build"
$dist = "dist"
$image = "image"
$basedir = "..\Packages"
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
# copy folder(s) needed for execution
$src_imagepath = @($currentdir, $image) -join "\"
$dst_imagepath = @($distpath, $appname, $image) -join "\"
Copy-Item $src_imagepath $dst_imagepath -Force -Recurse