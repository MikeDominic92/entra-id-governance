<#
.SYNOPSIS
    Create or update Conditional Access policy

.DESCRIPTION
    Creates a new MFA Conditional Access policy

.PARAMETER DisplayName
    Name of the policy

.PARAMETER State
    Policy state: enabled, disabled, or enabledForReportingButNotEnforced

.PARAMETER ExcludeBreakGlassAccount
    User ID of break glass account to exclude

.EXAMPLE
    .\Set-ConditionalAccessPolicy.ps1 -DisplayName "Require MFA for All Users" -State "enabledForReportingButNotEnforced"

.NOTES
    Requires Microsoft.Graph.Identity.SignIns module
    Requires Policy.ReadWrite.ConditionalAccess permission
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$DisplayName,

    [Parameter(Mandatory=$false)]
    [ValidateSet("enabled", "disabled", "enabledForReportingButNotEnforced")]
    [string]$State = "enabledForReportingButNotEnforced",

    [Parameter(Mandatory=$false)]
    [string]$ExcludeBreakGlassAccount
)

Import-Module Microsoft.Graph.Identity.SignIns -ErrorAction Stop

try {
    Write-Host "Connecting to Microsoft Graph..." -ForegroundColor Cyan
    Connect-MgGraph -Scopes "Policy.ReadWrite.ConditionalAccess" -NoWelcome

    # Prepare policy body
    $excludeUsers = @()
    if ($ExcludeBreakGlassAccount) {
        $excludeUsers += $ExcludeBreakGlassAccount
    }

    $policyBody = @{
        displayName = $DisplayName
        state = $State
        conditions = @{
            users = @{
                includeUsers = @("All")
                excludeUsers = $excludeUsers
            }
            applications = @{
                includeApplications = @("All")
            }
            clientAppTypes = @("all")
        }
        grantControls = @{
            operator = "OR"
            builtInControls = @("mfa")
        }
    }

    Write-Host "Creating Conditional Access policy: $DisplayName..." -ForegroundColor Cyan

    # Create the policy
    $policy = New-MgIdentityConditionalAccessPolicy -BodyParameter $policyBody

    Write-Host "`nPolicy Created Successfully!" -ForegroundColor Green
    Write-Host "============================" -ForegroundColor Green
    Write-Host "Policy ID: $($policy.Id)"
    Write-Host "Display Name: $($policy.DisplayName)"
    Write-Host "State: $($policy.State)" -ForegroundColor $(if ($State -eq "enabled") { "Green" } else { "Yellow" })
    Write-Host "`nNote: Policy is in $State mode." -ForegroundColor Cyan

    if ($State -ne "enabled") {
        Write-Host "Test the policy before enabling for enforcement." -ForegroundColor Yellow
    }

    Disconnect-MgGraph

} catch {
    Write-Error "Error creating policy: $_"
    exit 1
}
