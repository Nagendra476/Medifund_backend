from rest_framework import serializers

from .models import Donation


class DonationSerializer(serializers.ModelSerializer):

    donor_name = serializers.CharField(
        source="donor.username",
        read_only=True
    )

    campaign_title = serializers.CharField(
        source="campaign.title",
        read_only=True
    )

    class Meta:

        model = Donation
        fields = [
            "id",
            "donor",
            "campaign",
            "amount",
            "message",
            "created_at",
        ]