from django.urls import path
from .views import CampaignDonationsView, MyDonationsView, MyDonationsView
from .views import DonateView

urlpatterns = [

    path("donate/<int:id>/",DonateView.as_view()),
    path("campaign-donations/<int:id>/",CampaignDonationsView.as_view()),
    path("my-donations/", MyDonationsView.as_view()),

]