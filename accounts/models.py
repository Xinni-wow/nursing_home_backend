from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('relative', 'Relative'),   # 用户端亲属
        ('staff', 'Staff'),         # 管理端工作人员
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='relative')
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    security_question = models.CharField(max_length=255, blank=True, null=True)
    security_answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.user_type})'
