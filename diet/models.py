from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class DailyMenu(models.Model):
    MEAL_CHOICES = [
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
    ]

    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('date', 'meal_type')
        ordering = ['date', 'meal_type']

    def __str__(self):
        return f"{self.date} - {self.get_meal_type_display()}"
