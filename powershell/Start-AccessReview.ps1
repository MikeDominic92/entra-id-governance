<#
.SYNOPSIS
    Create and start an access review

.DESCRIPTION
    Creates a new access review for a specified group or application

.PARAMETER DisplayName
    Name of the access review

.PARAMETER GroupId
    ID of the group to review

.PARAMETER DurationDays
    Duration of the review in days (default 14)

.EXAMPLE
    .\Start-AccessReview.ps1 -DisplayName "Quarterly Admin Review" -GroupId "xxx-xxx-xxx" -DurationDays 14

.NOTES
    Requires Microsoft.Graph.Identity.Governance module
    Requires AccessReview.ReadWrite.All permission
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$DisplayName,

    [Parameter(Mandatory=$true)]
    [string]$GroupId,

    [Parameter(Mandatory=$false)]
    [int]$DurationDays = 14
)

Import-Module Microsoft.Graph.Identity.Governance -ErrorAction Stop

try {
    Write-Host "Connecting to Microsoft Graph..." -ForegroundColor Cyan
    Connect-MgGraph -Scopes "AccessReview.ReadWrite.All" -NoWelcome

    # Prepare review definition
    $reviewDefinition = @{
        displayName = $DisplayName
        scope = @{
            "@odata.type" = "#microsoft.graph.accessReviewQueryScope"
            query = "/groups/$GroupId/members"
            queryType = "MicrosoftGraph"
        }
        reviewers = @(
            @{
                query = "./manager"
                queryType = "MicrosoftGraph"
            }
        )
        settings = @{
            mailNotificationsEnabled = $true
            reminderNotificationsEnabled = $true
            justificationRequiredOnApproval = $true
            defaultDecisionEnabled = $false
            instanceDurationInDays = $DurationDays
            autoApplyDecisionsEnabled = $true
            recurrence = @{
                pattern = @{
                    type = "absoluteMonthly"
                    interval = 3
                }
                range = @{
                    type = "noEnd"
                    startDate = (Get-Date).ToString("yyyy-MM-dd")
                }
            }
        }
    }

    Write-Host "Creating access review: $DisplayName..." -ForegroundColor Cyan

    # Create the review
    $uri = "https://graph.microsoft.com/v1.0/identityGovernance/accessReviews/definitions"
    $review = Invoke-MgGraphRequest -Method POST -Uri $uri -Body ($reviewDefinition | ConvertTo-Json -Depth 10)

    Write-Host "`nAccess Review Created Successfully!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "Review ID: $($review.id)"
    Write-Host "Display Name: $($review.displayName)"
    Write-Host "Duration: $DurationDays days"
    Write-Host "Recurrence: Quarterly"
    Write-Host "`nReview will start automatically." -ForegroundColor Cyan

    Disconnect-MgGraph

} catch {
    Write-Error "Error creating access review: $_"
    exit 1
}
