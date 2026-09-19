from django.db import models

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, help_text="e.g., ₦500,000/month or Competitive")
    description = models.TextField(help_text="Full job responsibilities and requirements")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this job from the website")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {'Active' if self.is_active else 'Closed'}"