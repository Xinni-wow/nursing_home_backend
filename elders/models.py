from django.db import models
from accounts.models import CustomUser

class Elder(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='elders')
    photo = models.ImageField(upload_to='elder_photos/', null=True, blank=True)
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    id_number = models.CharField(max_length=18, unique=True)
    health_status = models.TextField()
    notes = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
