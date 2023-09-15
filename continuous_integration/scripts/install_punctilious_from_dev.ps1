$script = Split-Path $PSCommandPath -Leaf
$total_step = 1
$project_folder = "$Env:USERPROFILE\PycharmProjects\punctilious"
Set-Location $project_folder

$current_step = 1
Write-Output "Script: $script. Step: $current_step / $total_step. pip install -e $project_folder"
Invoke-Expression -Command "python -m pip install -e $project_folder"
