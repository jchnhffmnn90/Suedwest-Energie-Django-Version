from django.db import models

class Visit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10, default='GET')
    user_agent = models.TextField(blank=True, null=True)
    ip_address_anonymized = models.GenericIPAddressField(blank=True, null=True)
    referer = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Seitenaufruf'
        verbose_name_plural = 'Seitenaufrufe'

    def __str__(self):
        return f"{self.timestamp} - {self.path}"

