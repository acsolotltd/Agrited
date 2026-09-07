from django.db import models
from apps.accounts.models import EmailBasedUser
class BookingRequest(models.Model):
    PRODUCT_CHOICES = [
        ('Day Old Chicks', 'Day Old Chicks (Broiler / Layer)'),
        ('Premix & Feed', 'Premix & Feed Additives'),
        ('Vaccines', 'Vaccines & Medications'),
        ('Equipment', 'Farm Equipment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(EmailBasedUser, on_delete=models.CASCADE,)# default='Headquarters Dispatch')
    agent = models.CharField(max_length=150, default='Headquarters Dispatch')
    name = models.CharField(max_length=200, verbose_name="Full / Farm Name")
    phone = models.CharField(max_length=30)
    product = models.CharField(max_length=100, choices=PRODUCT_CHOICES, default='Day Old Chicks')
    quantity = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking Request"
        verbose_name_plural = "Booking Requests"

    def __str__(self):
        return f"{self.name} - {self.product} ({self.created_at.strftime('%Y-%m-%d')})"