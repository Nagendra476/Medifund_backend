from django.urls import path

from .views import (
AdminCampaignsView,
AdminDashboardStatsView,
ApproveCampaignView,
ApprovedCampaignsView,
CampaignDetailView,
CampaignDetailsView,
CreateCampaignView,
DonateView,
MyCampaignsView,
RejectCampaignView,
)

urlpatterns = [
# Create Campaign

path(
    "create/",
    CreateCampaignView.as_view()
),

# My Campaigns

path(
    "my-campaigns/",
    MyCampaignsView.as_view()
),

# Approved Campaigns

path(
    "approved-campaigns/",
    ApprovedCampaignsView.as_view()
),

# Campaign Details

path(
    "campaign-details/<int:pk>/",
    CampaignDetailsView.as_view()
),

# Donate

path(
    "donate/<int:pk>/",
    DonateView.as_view()
),

# Admin Dashboard Stats

path(
    "admin-dashboard-stats/",
    AdminDashboardStatsView.as_view()
),

# Admin Campaigns

path(
    "admin-campaigns/",
    AdminCampaignsView.as_view()
),

# Approve Campaign

path(
    "approve-campaign/<int:id>/",
    ApproveCampaignView.as_view()
),

# Reject Campaign

path(
    "reject-campaign/<int:id>/",
    RejectCampaignView.as_view()
),

# Single Campaign Edit/Delete

path(
    "<int:pk>/",
    CampaignDetailView.as_view()
),


]
