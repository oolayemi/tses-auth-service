from django.db import models


class AuditLog(models.Model):
    objects = models.Manager()
    event = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=1000)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event} by {self.email} at {self.created_at}"
