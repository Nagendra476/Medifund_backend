from accounts.models import User
from django.db import models
from accounts.models import User

class Campaign(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )


    title = models.CharField(max_length=200)

    description = models.TextField()

    goal_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    raised_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    image = models.ImageField(
        upload_to='campaign_images/'
    )

    medical_report = models.FileField(
        upload_to='medical_reports/'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
