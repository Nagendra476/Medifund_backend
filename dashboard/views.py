from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from campaigns.models import Campaign
from donations.models import Donation

from django.db.models import Sum, Count, F


from django.db.models.functions import TruncMonth

class DashboardStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_campaigns = Campaign.objects.count()

        approved_campaigns = Campaign.objects.filter(
            status="approved"
        ).count()

        pending_campaigns = Campaign.objects.filter(
            status="pending"
        ).count()

        rejected_campaigns = Campaign.objects.filter(
            status="rejected"
        ).count()

        completed_campaigns = Campaign.objects.filter(
            raised_amount__gte=F("goal_amount")
        ).count()

        total_donations = Donation.objects.count()

        total_amount = (
            Donation.objects.aggregate(total=Sum("amount"))["total"] or 0
        )

        total_donors = (
            Donation.objects.values("donor")
            .distinct()
            .count()
        )

        monthly_donations = (
            Donation.objects.annotate(month=TruncMonth("donated_at"))
            .values("month")
            .annotate(amount=Sum("amount"))
            .order_by("month")
        )

        monthly_data = []
        for entry in monthly_donations:
            if entry["month"]:
                month_name = entry["month"].strftime("%b")
                monthly_data.append({
                    "month": month_name,
                    "amount": float(entry["amount"])
                })

        return Response({
            "total_campaigns": total_campaigns,
            "approved_campaigns": approved_campaigns,
            "pending_campaigns": pending_campaigns,
            "rejected_campaigns": rejected_campaigns,
            "completed_campaigns": completed_campaigns,
            "total_donations": total_donations,
            "total_amount": total_amount,
            "total_donors": total_donors,
            "monthly_donations": monthly_data,
        })
    


from rest_framework.views import APIView
from rest_framework.response import Response
from campaigns.models import Campaign

class TopCampaignsView(APIView):

    def get(self, request):

        campaigns = Campaign.objects.order_by("-raised_amount")[:5]

        data = []

        for campaign in campaigns:
            data.append({
                "id": campaign.id,
                "title": campaign.title,
                "raised_amount": campaign.raised_amount,
                "goal_amount": campaign.goal_amount,
            })

        return Response(data)
class RecentDonationsView(APIView):

    def get(self, request):

        donations = Donation.objects.select_related(
            "campaign",
            "donor"
        ).order_by("-donated_at")[:5]

        data = []

        for donation in donations:

            data.append({

                "donor": donation.donor.username,
                "campaign": donation.campaign.title,
                "amount": donation.amount,
                "date": donation.donated_at.strftime("%d %b %Y")

            })

        return Response(data)