from django.db import models
from elders.models import Elder
from django.utils import timezone

class HealthRecord(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField(default=timezone.now)

    temperature = models.FloatField(null=True, blank=True, help_text="单位：°C")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True, help_text="收缩压，单位：mmHg")
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True, help_text="舒张压，单位：mmHg")
    heart_rate = models.IntegerField(null=True, blank=True, help_text="单位：bpm")
    blood_sugar = models.FloatField(null=True, blank=True, help_text="空腹血糖，单位：mmol/L")
    respiratory_rate = models.IntegerField(null=True, blank=True, help_text="单位：次/分钟")
    oxygen_saturation = models.FloatField(null=True, blank=True, help_text="单位：%")
    weight = models.FloatField(null=True, blank=True, help_text="单位：kg")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('elder', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.elder.full_name} - {self.date}"
