from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CampaignSerializer


class CreateCampaignView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CampaignSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                created_by=request.user
            )

            return Response({

                "message":
                "Campaign Created Successfully"

            }, status=201)

        return Response(
            serializer.errors,
            status=400
        )
from .models import Campaign

class MyCampaignsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        campaigns = Campaign.objects.filter(
            created_by=request.user
        ).order_by("-created_at")

        serializer = CampaignSerializer(
            campaigns,
            many=True
        )

        return Response(serializer.data)
from .models import Campaign

class CampaignDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            if request.user.role == 'admin':
                campaign = Campaign.objects.get(id=pk)
            else:
                campaign = Campaign.objects.get(
                    id=pk,
                    created_by=request.user
                )

        except Campaign.DoesNotExist:

            return Response({

                "error": "Campaign Not Found"

            }, status=404)

        serializer = CampaignSerializer(

            campaign,
            data=request.data,
            partial=True

        )

        if serializer.is_valid():

            serializer.save()

            return Response({

                "message":
                "Campaign Updated Successfully"

            })

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        try:

            if request.user.role == 'admin':
                campaign = Campaign.objects.get(id=pk)
            else:
                campaign = Campaign.objects.get(
                    id=pk,
                    created_by=request.user
                )

        except Campaign.DoesNotExist:

            return Response({

                "error": "Campaign Not Found"

            }, status=404)

        campaign.delete()

        return Response({

            "message":
            "Campaign Deleted Successfully"

        })
    def get(self, request, pk):

        try:

            if request.user.role == 'admin':
                campaign = Campaign.objects.get(id=pk)
            else:
                campaign = Campaign.objects.get(
                    id=pk,
                    created_by=request.user
                )

        except Campaign.DoesNotExist:

            return Response({

                "error": "Campaign Not Found"

            }, status=404)

        serializer = CampaignSerializer(campaign)

        return Response(serializer.data)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Campaign
from .serializers import CampaignSerializer


class AdminCampaignsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        campaigns = Campaign.objects.all().order_by("-created_at")

        serializer = CampaignSerializer(
            campaigns,
            many=True
        )

        return Response(serializer.data)

    def patch(self, request, pk):

        try:

            campaign = Campaign.objects.get(id=pk)

        except Campaign.DoesNotExist:

            return Response({

                "error": "Campaign Not Found"

            }, status=404)

        status_value = request.data.get("status")

        campaign.status = status_value

        campaign.save()

        return Response({

            "message":
            "Campaign Status Updated"

        })
class ApprovedCampaignsView(APIView):

    def get(self, request):

        campaigns = Campaign.objects.filter(
            status="approved"
        ).order_by("-created_at")

        serializer = CampaignSerializer(
            campaigns,
            many=True
        )

        return Response(serializer.data)
    
class CampaignDetailsView(APIView):

    def get(self, request, pk):

        try:

            campaign = Campaign.objects.get(id=pk)

        except Campaign.DoesNotExist:

            return Response({

                "error":
                "Campaign not found"

            }, status=404)

        serializer = CampaignSerializer(campaign)

        return Response(serializer.data)
from donations.models import Donation
class DonateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            campaign = Campaign.objects.get(id=pk)

        except Campaign.DoesNotExist:

            return Response({

                "error":
                "Campaign not found"

            }, status=404)

        amount = request.data.get("amount")

        # Create Donation

        Donation.objects.create(

            donor=request.user,
            campaign=campaign,
            amount=amount

        )

        # Update Raised Amount

        campaign.raised_amount += float(amount)

        campaign.save()

        return Response({

            "message":
            "Donation Successful"

        })
from rest_framework.permissions import IsAuthenticated

# Admin View All Campaigns

class AdminCampaignsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        campaigns = Campaign.objects.all().order_by("-id")

        serializer = CampaignSerializer(
            campaigns,
            many=True
        )

        return Response(serializer.data)
class ApproveCampaignView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, id):

        campaign = Campaign.objects.get(id=id)

        campaign.status = "approved"

        campaign.save()

        return Response({
            "message": "Campaign Approved"
        })
class RejectCampaignView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, id):

        campaign = Campaign.objects.get(id=id)

        campaign.status = "rejected"

        campaign.save()

        return Response({
            "message": "Campaign Rejected"
        })
from rest_framework.permissions import IsAuthenticated
from campaigns.models import Campaign
from donations.models import Donation
from accounts.models import User

from django.db.models import Sum

class AdminDashboardStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_users = User.objects.count()

        total_campaigns = Campaign.objects.count()

        approved_campaigns = Campaign.objects.filter(
            status="approved"
        ).count()

        pending_campaigns = Campaign.objects.filter(
            status="pending"
        ).count()

        total_donations = Donation.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0

        return Response({

            "total_users": total_users,

            "total_campaigns": total_campaigns,

            "approved_campaigns": approved_campaigns,

            "pending_campaigns": pending_campaigns,

            "total_donations": total_donations

        })