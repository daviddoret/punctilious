# This Powershell script roughly mimics the ReadTheDocs build scripts,
# but the build is executed locally from the dev environment.
# The key idea is to build the docs but simultaneously to verify
# that the ReadTheDocs build should be successful.
$InformationPreference = "Continue";
$total_step = 8
$script = Split-Path $PSCommandPath -Leaf
Write-Information "Script: $( $script )."
$script_folder = $PSScriptRoot
$ci_folder = Split-Path -Path $script_folder -Parent
$project_folder = Split-Path -Path $ci_folder -Parent
$docs_folder = "$( $project_folder )\docs"
$docs_source_folder = "$( $docs_folder )\source"
$docs_build_folder = "$( $docs_folder )\build"
Write-Information "Script: $( $script ). project_folder = $( $project_folder )"
Write-Information "Script: $( $script ). docs_source_folder = $( $docs_source_folder )"
Write-Information "Script: $( $script ). docs_build_folder = $( $docs_build_folder )"

$current_step = 1
Write-Information "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). start_venv.ps1"
$environment_directory = & $PSScriptRoot\start_venv.ps1
Write-Information "Script: $( $script ). Python virtual environment: $( $environment_directory )."

$current_step = 8
Write-Information "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). stop_env.ps1"
& $PSScriptRoot\stop_venv.ps1 -EnvironmentDirectory $environment_directory
