from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from campaigns.models import Campaign
from .models import Payment
import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreateOrderView(APIView):

    def post(self, request):
        try:
            campaign_id = request.data.get("campaign_id")
            amount = request.data.get("amount")

            if not campaign_id or not amount:
                return Response(
                    {"error": "Campaign ID and Amount are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            campaign = Campaign.objects.get(id=campaign_id)

            # Razorpay expects amount in paise
            amount_in_paise = int(float(amount) * 100)

            order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1
            })

            payment = Payment.objects.create(
                donor=request.user,
                campaign=campaign,
                amount=amount,
                razorpay_order_id=order["id"],
                status="Pending"
            )

            return Response({
                "success": True,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "payment_id": payment.id
            })

        except Campaign.DoesNotExist:
            return Response(
                {"error": "Campaign not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from rest_framework.permissions import IsAuthenticated
from donations.models import Donation
from decimal import Decimal


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response(
                {"error": "All payment details are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            params = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }

            # Verify Signature
            client.utility.verify_payment_signature(params)

            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = "Success"
            payment.save()

            campaign = payment.campaign
            campaign.raised_amount += Decimal(payment.amount)
            campaign.save()

            Donation.objects.create(
                donor=request.user,
                campaign=campaign,
                amount=payment.amount
            )

            return Response({
                "success": True,
                "message": "Payment Verified Successfully"
            })

        except razorpay.errors.SignatureVerificationError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Payment Signature"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Payment.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Payment Record Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )