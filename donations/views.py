from decimal import Decimal

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from campaigns.models import Campaign
from .models import Donation
from .serializers import DonationSerializer
class DonateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        try:

            # Get Campaign
            campaign = Campaign.objects.get(id=id)

                        # Get Donation Amount
            amount = request.data.get("amount")

            # Get Donation Message (Optional)
            message = request.data.get("message", "")
                        

            # Check if campaign is already completed
            if campaign.raised_amount >= campaign.goal_amount:

                return Response(
                    {
                        "error": "This campaign has already reached its goal. Donations are closed."
                    },
                    status=400
                )

            # Validate amount
            if not amount:

                return Response(
                    {
                        "error": "Donation amount is required."
                    },
                    status=400
                )

            amount = Decimal(amount)

            if amount <= 0:

                return Response(
                    {
                        "error": "Donation amount must be greater than 0."
                    },
                    status=400
                )

            # Create Donation
            # Create Donation
            Donation.objects.create(
                donor=request.user,
                campaign=campaign,
                amount=amount,
                message=message
            )

            # Update Raised Amount
            campaign.raised_amount += amount

            # Prevent raised amount from exceeding goal amount
            if campaign.raised_amount > campaign.goal_amount:
                campaign.raised_amount = campaign.goal_amount

            campaign.save()

            return Response({

                "message": "Donation Successful",

                "raised_amount": campaign.raised_amount,

                "goal_amount": campaign.goal_amount,

                "campaign_completed": campaign.raised_amount >= campaign.goal_amount,

                "donation_message": message

            })

        except Campaign.DoesNotExist:

            return Response(
                {
                    "error": "Campaign not found."
                },
                status=404
            )

        except Exception as e:

            print(e)

            return Response(
                {
                    "error": str(e)
                },
                status=400
            )
        
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Donation
from .serializers import DonationSerializer


class CampaignDonationsView(APIView):

    def get(self, request, id):

        donations = Donation.objects.filter(
            campaign_id=id
        ).order_by("-donated_at")

        serializer = DonationSerializer(
            donations,
            many=True
        )

        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Donation
from .serializers import DonationSerializer
from .serializers import DonationSerializer
from .models import Donation

class MyDonationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        donations = Donation.objects.filter(
            donor=request.user
        ).order_by("-donated_at")

        serializer = DonationSerializer(
            donations,
            many=True
        )

        return Response(serializer.data)