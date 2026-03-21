from django.db import models
from django.contrib.auth.models import User


class Lead(models.Model):
    AI_STATUS_CHOICES = [
        ("Hot", "Hot"),
        ("Warm", "Warm"),
        ("Cold", "Cold"),
    ]

    CRM_STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Qualified", "Qualified"),
        ("Converted", "Converted"),
        ("Lost", "Lost"),
    ]

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    source = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)

    budget = models.IntegerField()
    interaction_score = models.IntegerField()
    interaction_history = models.TextField(blank=True, null=True)
    company_size = models.IntegerField()

    lead_score = models.FloatField(default=0)
    conversion_probability = models.FloatField(default=0)

    status = models.CharField(max_length=10, choices=AI_STATUS_CHOICES, default="Cold")
    crm_status = models.CharField(max_length=20, choices=CRM_STATUS_CHOICES, default="New")

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InteractionLog(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="interaction_logs")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"