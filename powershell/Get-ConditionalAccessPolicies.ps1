<#
.SYNOPSIS
    Retrieve and analyze Conditional Access policies

.DESCRIPTION
    Connects to Microsoft Graph and retrieves all Conditional Access policies
    with detailed analysis and reporting

.PARAMETER ExportPath
    Optional path to export results to JSON

.EXAMPLE
    .\Get-ConditionalAccessPolicies.ps1
    .\Get-ConditionalAccessPolicies.ps1 -ExportPath "C:\Reports\ca_policies.json"

.NOTES
    Requires Microsoft.Graph.Identity.SignIns module
    Requires Conditional Access read permissions
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ExportPath
)

# Import required module
Import-Module Microsoft.Graph.Identity.SignIns -ErrorAction Stop

try {
    # Connect to Microsoft Graph
    Write-Host "Connecting to Microsoft Graph..." -ForegroundColor Cyan
    Connect-MgGraph -Scopes "Policy.Read.All" -NoWelcome

    # Get all Conditional Access policies
    Write-Host "Fetching Conditional Access policies..." -ForegroundColor Cyan
    $policies = Get-MgIdentityConditionalAccessPolicy -All

    # Analyze policies
    $enabled = ($policies | Where-Object { $_.State -eq "enabled" }).Count
    $disabled = ($policies | Where-Object { $_.State -eq "disabled" }).Count
    $reportOnly = ($policies | Where-Object { $_.State -eq "enabledForReportingButNotEnforced" }).Count

    # Check for MFA requirement
    $mfaPolicies = $policies | Where-Object {
        $_.State -eq "enabled" -and
        $_.GrantControls.BuiltInControls -contains "mfa"
    }

    # Check for legacy auth blocking
    $legacyAuthBlocked = $policies | Where-Object {
        $_.State -eq "enabled" -and
        $_.Conditions.ClientAppTypes -contains "exchangeActiveSync"
    }

    # Display summary
    Write-Host "`nConditional Access Policy Summary:" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "Total Policies: $($policies.Count)"
    Write-Host "Enabled: $enabled" -ForegroundColor Green
    Write-Host "Disabled: $disabled" -ForegroundColor Yellow
    Write-Host "Report Only: $reportOnly" -ForegroundColor Cyan
    Write-Host "`nMFA Policies: $($mfaPolicies.Count)" -ForegroundColor Green
    Write-Host "Legacy Auth Blocked: $($legacyAuthBlocked.Count)" -ForegroundColor Green

    # Display policy details
    Write-Host "`nPolicy Details:" -ForegroundColor Cyan
    foreach ($policy in $policies) {
        $statusColor = switch ($policy.State) {
            "enabled" { "Green" }
            "disabled" { "Red" }
            "enabledForReportingButNotEnforced" { "Yellow" }
        }

        Write-Host "`n  Name: $($policy.DisplayName)" -ForegroundColor White
        Write-Host "  ID: $($policy.Id)" -ForegroundColor Gray
        Write-Host "  State: $($policy.State)" -ForegroundColor $statusColor

        if ($policy.GrantControls.BuiltInControls) {
            Write-Host "  Controls: $($policy.GrantControls.BuiltInControls -join ', ')" -ForegroundColor Cyan
        }
    }

    # Export if requested
    if ($ExportPath) {
        $policies | ConvertTo-Json -Depth 10 | Out-File -FilePath $ExportPath -Encoding UTF8
        Write-Host "`nPolicies exported to: $ExportPath" -ForegroundColor Green
    }

    # Disconnect
    Disconnect-MgGraph

} catch {
    Write-Error "Error: $_"
    exit 1
}
