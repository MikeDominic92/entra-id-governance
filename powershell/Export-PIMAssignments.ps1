<#
.SYNOPSIS
    Export PIM role assignments

.DESCRIPTION
    Exports eligible and active PIM role assignments with analysis

.PARAMETER ExportPath
    Path to export CSV results

.EXAMPLE
    .\Export-PIMAssignments.ps1 -ExportPath "C:\Reports\pim_assignments.csv"

.NOTES
    Requires Microsoft.Graph.Identity.Governance module
    Requires RoleManagement.Read.All permission
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ExportPath = "pim_assignments.csv"
)

Import-Module Microsoft.Graph.Identity.Governance -ErrorAction Stop

try {
    Write-Host "Connecting to Microsoft Graph..." -ForegroundColor Cyan
    Connect-MgGraph -Scopes "RoleManagement.Read.All" -NoWelcome

    # Get role definitions
    Write-Host "Fetching role definitions..." -ForegroundColor Cyan
    $roleDefinitions = Get-MgRoleManagementDirectoryRoleDefinition -All

    # Create role lookup
    $roleMap = @{}
    foreach ($role in $roleDefinitions) {
        $roleMap[$role.Id] = $role.DisplayName
    }

    # Get eligible assignments
    Write-Host "Fetching eligible (PIM) assignments..." -ForegroundColor Cyan
    $eligibleUrl = "https://graph.microsoft.com/v1.0/roleManagement/directory/roleEligibilityScheduleInstances"
    $eligible = Invoke-MgGraphRequest -Method GET -Uri $eligibleUrl
    $eligibleAssignments = $eligible.value

    # Get active assignments
    Write-Host "Fetching active assignments..." -ForegroundColor Cyan
    $activeUrl = "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignmentScheduleInstances"
    $active = Invoke-MgGraphRequest -Method GET -Uri $activeUrl
    $activeAssignments = $active.value

    # Prepare export data
    $exportData = @()

    foreach ($assignment in $eligibleAssignments) {
        $exportData += [PSCustomObject]@{
            Type = "Eligible"
            PrincipalId = $assignment.principalId
            RoleName = $roleMap[$assignment.roleDefinitionId]
            RoleId = $assignment.roleDefinitionId
            StartDateTime = $assignment.startDateTime
            EndDateTime = $assignment.endDateTime
            AssignmentId = $assignment.id
        }
    }

    foreach ($assignment in $activeAssignments) {
        $exportData += [PSCustomObject]@{
            Type = "Active"
            PrincipalId = $assignment.principalId
            RoleName = $roleMap[$assignment.roleDefinitionId]
            RoleId = $assignment.roleDefinitionId
            StartDateTime = $assignment.startDateTime
            EndDateTime = $assignment.endDateTime
            AssignmentId = $assignment.id
        }
    }

    # Display summary
    Write-Host "`nPIM Assignment Summary:" -ForegroundColor Green
    Write-Host "======================" -ForegroundColor Green
    Write-Host "Eligible Assignments: $($eligibleAssignments.Count)" -ForegroundColor Cyan
    Write-Host "Active Assignments: $($activeAssignments.Count)" -ForegroundColor Yellow

    # Detect standing access
    $standingAccess = $activeAssignments | Where-Object {
        -not $_.endDateTime -or
        ([DateTime]$_.endDateTime - [DateTime]::Now).Days -gt 365
    }

    if ($standingAccess.Count -gt 0) {
        Write-Host "`nWARNING: $($standingAccess.Count) standing admin assignments detected!" -ForegroundColor Red
    }

    # Export to CSV
    $exportData | Export-Csv -Path $ExportPath -NoTypeInformation -Encoding UTF8
    Write-Host "`nAssignments exported to: $ExportPath" -ForegroundColor Green

    # Disconnect
    Disconnect-MgGraph

} catch {
    Write-Error "Error: $_"
    exit 1
}
