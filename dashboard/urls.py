from django.urls import path
from .views import DashboardStatisticsView, TopCampaignsView, RecentDonationsView

urlpatterns = [
    path("statistics/", DashboardStatisticsView.as_view()),
    path("top-campaigns/", TopCampaignsView.as_view()),
    path("recent-donations/", RecentDonationsView.as_view()),
]