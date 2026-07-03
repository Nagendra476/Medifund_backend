from django.db import models
from accounts.models import User
from campaigns.models import Campaign

class Donation(models.Model):

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    donated_at = models.DateTimeField(
        auto_now_add=True
    )
    message = models.TextField(blank=True, null=True)